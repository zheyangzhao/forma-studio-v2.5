"""Sprint 2B ImageEditPanel 行為測試。

對應 PLAN-sprint-2.md §3.5：
- test_image_edit_requires_reference
- test_image_generate_uses_quality
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.widgets.image_edit_panel import ImageEditPanel


def _no_client() -> None:
    raise RuntimeError("client_factory not expected to be called")


def test_image_edit_requires_reference(qtbot) -> None:
    """點修改既有圖時若沒 reference，應 emit error 而不呼叫 client。"""
    panel = ImageEditPanel(client_factory=_no_client)
    qtbot.addWidget(panel)
    panel.set_prompt("just words")
    errors: list[str] = []
    panel.error_raised.connect(errors.append)
    panel._on_edit_clicked()  # validation 應在 dispatch 前 fail
    assert any("至少 1 張參考圖" in e for e in errors)


def test_image_edit_requires_prompt(qtbot) -> None:
    panel = ImageEditPanel(client_factory=_no_client)
    qtbot.addWidget(panel)
    errors: list[str] = []
    panel.error_raised.connect(errors.append)
    panel._on_edit_clicked()
    assert any("prompt" in e for e in errors)


def test_image_generate_requires_prompt(qtbot) -> None:
    panel = ImageEditPanel(client_factory=_no_client)
    qtbot.addWidget(panel)
    errors: list[str] = []
    panel.error_raised.connect(errors.append)
    panel._on_generate_clicked()
    assert any("prompt" in e for e in errors)


def test_image_generate_uses_quality(qtbot, monkeypatch) -> None:
    """點生成新圖時 quality 應傳到 generate_image() call。"""
    captured: dict = {}

    def fake_factory():
        client = MagicMock()
        client.generate_image = MagicMock()
        client.close = MagicMock()
        return client

    panel = ImageEditPanel(client_factory=fake_factory)
    qtbot.addWidget(panel)
    panel.set_prompt("a futuristic skyline")
    panel.quality_dial.set_quality("high")
    # Stub _dispatch 不真開 thread，但確認 task_factory 會 build 出 (client, coro)
    captured_factory = []
    panel._dispatch = lambda factory: captured_factory.append(factory)
    panel._on_generate_clicked()
    assert captured_factory, "expected _dispatch called"
    factory = captured_factory[0]
    client, coro = factory()
    # coro 是 coroutine；不真 await，只看 client.generate_image 是否被排程
    coro.close()
    client.generate_image.assert_called_once()
    _, kwargs = client.generate_image.call_args
    assert kwargs.get("quality") == "high"


def test_image_panel_set_design_memory(qtbot) -> None:
    """set_design_memory 接受 None 與 DesignMemory 都不 crash。"""
    from app.utils.design_memory import DesignMemory

    panel = ImageEditPanel(client_factory=_no_client)
    qtbot.addWidget(panel)
    panel.set_design_memory(None)
    panel.set_design_memory(DesignMemory(brand_name="ACME"))
    # 內部保存
    assert panel._memory is not None
    assert panel._memory.brand_name == "ACME"
