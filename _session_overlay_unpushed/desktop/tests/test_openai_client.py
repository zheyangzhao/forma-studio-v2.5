"""Sprint 2A OpenAI client mock test（generations / edits / enhance + 401/413/429）。

對應 PLAN-sprint-2.md §2.4 / §2.8 / §6.2。
使用 respx mock httpx，不打真 API。
"""

from __future__ import annotations

import asyncio
import base64
from pathlib import Path

import httpx
import pytest
import respx

from app.api.openai_client import OpenAIClient, OpenAIClientError


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


@pytest.fixture
def fake_png(tmp_path: Path) -> Path:
    p = tmp_path / "ref.png"
    # 8-byte minimal PNG header；mock 不真解碼
    p.write_bytes(b"\x89PNG\r\n\x1a\n")
    return p


@respx.mock
def test_generate_image_calls_correct_url() -> None:
    route = respx.post("https://api.openai.com/v1/images/generations").mock(
        return_value=httpx.Response(
            200, json={"data": [{"b64_json": _b64(b"fake-png")}]}
        )
    )
    client = OpenAIClient(api_key="sk-test")
    result = asyncio.run(
        client.generate_image("hello", quality="medium", size="1024x1024")
    )
    asyncio.run(client.close())
    assert route.called
    body = route.calls[0].request.read()
    assert b'"quality": "medium"' in body or b'"quality":"medium"' in body
    assert b'"model": "gpt-image-2"' in body or b'"model":"gpt-image-2"' in body
    assert len(result) == 1
    assert result[0].data == b"fake-png"


@respx.mock
def test_edit_image_uses_edits_endpoint(fake_png: Path) -> None:
    route = respx.post("https://api.openai.com/v1/images/edits").mock(
        return_value=httpx.Response(
            200, json={"data": [{"b64_json": _b64(b"edited")}]}
        )
    )
    client = OpenAIClient(api_key="sk-test")
    result = asyncio.run(client.edit_image("change", [fake_png], quality="high"))
    asyncio.run(client.close())
    assert route.called
    assert result.data == b"edited"


def test_edit_image_rejects_zero_or_too_many(fake_png: Path) -> None:
    client = OpenAIClient(api_key="sk-test")
    with pytest.raises(ValueError):
        asyncio.run(client.edit_image("x", []))
    with pytest.raises(ValueError):
        asyncio.run(client.edit_image("x", [fake_png] * 5))
    asyncio.run(client.close())


def test_edit_image_rejects_non_png_mask(fake_png: Path, tmp_path: Path) -> None:
    bad_mask = tmp_path / "x.jpg"
    bad_mask.write_bytes(b"not png")
    client = OpenAIClient(api_key="sk-test")
    with pytest.raises(ValueError, match="PNG"):
        asyncio.run(client.edit_image("x", [fake_png], mask=bad_mask))
    asyncio.run(client.close())


@respx.mock
def test_generate_image_401_friendly_error() -> None:
    respx.post("https://api.openai.com/v1/images/generations").mock(
        return_value=httpx.Response(401, json={"error": {"message": "bad key"}})
    )
    client = OpenAIClient(api_key="sk-test")
    with pytest.raises(OpenAIClientError, match="API Key 無效"):
        asyncio.run(client.generate_image("x"))
    asyncio.run(client.close())


@respx.mock
def test_generate_image_413_friendly_error() -> None:
    respx.post("https://api.openai.com/v1/images/generations").mock(
        return_value=httpx.Response(413, text="payload too large")
    )
    client = OpenAIClient(api_key="sk-test")
    with pytest.raises(OpenAIClientError, match="圖片太大"):
        asyncio.run(client.generate_image("x"))
    asyncio.run(client.close())


@respx.mock
def test_generate_image_429_friendly_error() -> None:
    respx.post("https://api.openai.com/v1/images/generations").mock(
        return_value=httpx.Response(429, text="rate limit")
    )
    client = OpenAIClient(api_key="sk-test")
    with pytest.raises(OpenAIClientError, match="速率限制"):
        asyncio.run(client.generate_image("x"))
    asyncio.run(client.close())


@respx.mock
def test_enhance_prompt_calls_chat_completions() -> None:
    route = respx.post("https://api.openai.com/v1/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={"choices": [{"message": {"content": "improved prompt"}}]},
        )
    )
    client = OpenAIClient(api_key="sk-test")
    result = asyncio.run(client.enhance_prompt("draft prompt"))
    asyncio.run(client.close())
    assert route.called
    body = route.calls[0].request.read()
    assert b"gpt-4o-mini" in body
    assert result == "improved prompt"


def test_init_rejects_empty_key() -> None:
    with pytest.raises(ValueError):
        OpenAIClient(api_key="")
    with pytest.raises(ValueError):
        OpenAIClient(api_key="   ")
