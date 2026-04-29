"""OpenAI client 封裝（generations + edits + chat completions）。

對應 SDD-v2.5 §4.1 edit endpoint、Tier 1.6 enhance prompt。
PLAN-sprint-2.md §2.4。
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path

import httpx


class OpenAIClientError(RuntimeError):
    """OpenAI API 呼叫失敗的統一例外。"""


@dataclass(frozen=True)
class ImageResult:
    data: bytes
    mime_type: str = "image/png"


# 對應 web/forma-studio.html 的 ENHANCE_SYSTEM_PROMPT，桌面版同源
ENHANCE_SYSTEM_PROMPT = """你是 Forma Studio 的 prompt 增強器。
依 craft.md §19 final audit 把使用者 prompt 改寫得更完整。
輸出僅包含改寫後 prompt，不含說明。

必須補強：
1. 任務意圖：image / edit / infographic / prototype / brand。
2. 受眾、渠道、決策情境。
3. 核心訊息一句話。
4. 構圖、版面、typography、color system、material / lighting。
5. in-image text 必須用引號逐字列出。
6. size、quality、negative constraints。
7. 反 AI Slop：禁紫漸變、generic card wall、emoji 圖標、假 logo、不可讀文字。
8. 若原 prompt 含 source attribution，必須保留。

不要新增未提供的具體品牌、人物、日期、法規或產品版本。若缺資訊，用 [PLACEHOLDER: ...] 標記。"""


def _guess_mime(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"
    return "image/png"


def _format_api_error(resp: httpx.Response) -> str:
    body = resp.text[:300]
    if resp.status_code == 401:
        return "API Key 無效或已過期"
    if resp.status_code == 413:
        return "圖片太大，請縮小到 2048px 內再試"
    if resp.status_code == 429:
        return "OpenAI API 速率限制，請稍候再試"
    return f"OpenAI API error {resp.status_code}: {body}"


class OpenAIClient:
    BASE_URL = "https://api.openai.com/v1"
    IMAGE_MODEL = "gpt-image-2"
    TEXT_MODEL = "gpt-4o-mini"

    def __init__(
        self,
        api_key: str,
        *,
        timeout: float = 120.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not api_key.strip():
            raise ValueError("api_key is required")
        self._key = api_key.strip()
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(timeout=timeout)

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._key}"}

    async def generate_image(
        self,
        prompt: str,
        *,
        size: str = "1024x1024",
        quality: str = "medium",
        n: int = 1,
    ) -> list[ImageResult]:
        # SDD §4.1：generations 與 edits 分開 endpoint
        payload = {
            "model": self.IMAGE_MODEL,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": n,
            "response_format": "b64_json",
        }
        resp = await self._client.post(
            f"{self.BASE_URL}/images/generations",
            headers=self._headers(),
            json=payload,
        )
        return self._decode_image_response(resp)

    async def edit_image(
        self,
        prompt: str,
        images: list[Path],
        mask: Path | None = None,
        *,
        size: str = "1024x1024",
        quality: str = "medium",
    ) -> ImageResult:
        # SDD §4.1：最多 4 張 reference images，mask 為 PNG alpha
        if not images:
            raise ValueError("edit_image requires at least one reference image")
        if len(images) > 4:
            raise ValueError("edit_image supports at most 4 reference images")
        if mask is not None and mask.suffix.lower() != ".png":
            # SDD §4.1：mask 必須是 PNG alpha；非 PNG 直接拒絕，避免 API 才回錯
            raise ValueError("mask must be a PNG file with alpha channel")

        files: list[tuple[str, tuple[str, bytes, str]]] = []
        for image_path in images:
            files.append(
                (
                    "image[]",
                    (image_path.name, image_path.read_bytes(), _guess_mime(image_path)),
                )
            )
        if mask:
            files.append(("mask", (mask.name, mask.read_bytes(), "image/png")))

        data = {
            "model": self.IMAGE_MODEL,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "response_format": "b64_json",
        }
        resp = await self._client.post(
            f"{self.BASE_URL}/images/edits",
            headers=self._headers(),
            data=data,
            files=files,
        )
        results = self._decode_image_response(resp)
        if not results:
            raise OpenAIClientError("OpenAI 回傳空結果")
        return results[0]

    async def enhance_prompt(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float = 0.2,
    ) -> str:
        # 對應 Tier 1.6 web 版 enhancePromptWithOpenAI()
        payload = {
            "model": self.TEXT_MODEL,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt or ENHANCE_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        }
        resp = await self._client.post(
            f"{self.BASE_URL}/chat/completions",
            headers=self._headers(),
            json=payload,
        )
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise OpenAIClientError(_format_api_error(exc.response)) from exc
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

    def _decode_image_response(self, resp: httpx.Response) -> list[ImageResult]:
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise OpenAIClientError(_format_api_error(exc.response)) from exc
        payload = resp.json()
        return [
            ImageResult(data=base64.b64decode(item["b64_json"]))
            for item in payload.get("data", [])
            if item.get("b64_json")
        ]
