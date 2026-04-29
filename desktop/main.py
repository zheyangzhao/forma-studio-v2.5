"""Forma Studio v2.5 桌面版入口。

對應 PLAN-sprint-2.md §2.1 / SDD §四 Tier 2。
"""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from app.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Forma Studio")
    app.setOrganizationName("Forma Studio")

    icon_path = Path(__file__).resolve().parent / "assets" / "forma-studio.icns"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow(project_root=Path(__file__).resolve().parents[1])
    window.resize(1180, 820)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
