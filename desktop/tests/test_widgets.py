"""Sprint 2B widget tests（pytest-qt）。

對應 PLAN-sprint-2.md §3.5。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.widgets.mask_uploader import MaskUploader, validate_png_alpha
from app.widgets.reference_drop_zone import ReferenceDropZone


def test_validate_png_alpha_rejects_non_png(tmp_path: Path) -> None:
    fake_jpg = tmp_path / "x.jpg"
    fake_jpg.write_bytes(b"not png")
    ok, msg = validate_png_alpha(fake_jpg)
    assert ok is False
    assert "png" in msg.lower() or "PNG" in msg


def test_validate_png_alpha_handles_missing(tmp_path: Path) -> None:
    ok, msg = validate_png_alpha(tmp_path / "missing.png")
    assert ok is False
    assert "不存在" in msg


def test_validate_png_alpha_rejects_non_alpha_png(tmp_path: Path, qtbot) -> None:
    from PyQt6.QtGui import QImage
    img = QImage(64, 64, QImage.Format.Format_RGB888)
    img.fill(0xFFFFFFFF)
    out = tmp_path / "rgb.png"
    img.save(str(out), "PNG")
    ok, msg = validate_png_alpha(out)
    assert ok is False
    assert "alpha" in msg.lower()


def test_validate_png_alpha_accepts_alpha_png(tmp_path: Path, qtbot) -> None:
    from PyQt6.QtGui import QImage
    img = QImage(32, 32, QImage.Format.Format_ARGB32)
    img.fill(0)  # 全透明
    out = tmp_path / "alpha.png"
    img.save(str(out), "PNG")
    ok, msg = validate_png_alpha(out)
    assert ok is True
    assert msg == ""


def test_reference_drop_zone_limits_to_four(tmp_path: Path, qtbot) -> None:
    zone = ReferenceDropZone()
    qtbot.addWidget(zone)
    paths = []
    for i in range(6):
        p = tmp_path / f"img{i}.png"
        p.write_bytes(b"\x89PNG\r\n\x1a\n")
        paths.append(p)
    zone.add_paths(paths)
    assert len(zone.image_paths()) == 4


def test_reference_drop_zone_skips_invalid_suffix(tmp_path: Path, qtbot) -> None:
    zone = ReferenceDropZone()
    qtbot.addWidget(zone)
    gif = tmp_path / "anim.gif"
    gif.write_bytes(b"GIF89a")
    png = tmp_path / "ok.png"
    png.write_bytes(b"\x89PNG\r\n\x1a\n")
    zone.add_paths([gif, png])
    assert zone.image_paths() == [png]


def test_mask_uploader_clears_on_invalid(tmp_path: Path, qtbot) -> None:
    from PyQt6.QtGui import QImage
    uploader = MaskUploader()
    qtbot.addWidget(uploader)
    # 先設一個 valid alpha mask
    img = QImage(16, 16, QImage.Format.Format_ARGB32)
    img.fill(0)
    valid = tmp_path / "valid.png"
    img.save(str(valid), "PNG")
    uploader.set_mask(valid)
    assert uploader.mask_path() == valid
    # 再設 invalid → 應清掉舊 mask
    invalid = tmp_path / "x.jpg"
    invalid.write_bytes(b"x")
    uploader.set_mask(invalid)
    assert uploader.mask_path() is None
