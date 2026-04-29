"""系統鑰匙圈封裝。

對應 CLAUDE.md：桌面版 API Key 一律使用 keyring 存系統鑰匙圈，
service="Forma Studio"、account="openai_api_key"。

PLAN-sprint-2.md §2.3。
"""

from __future__ import annotations

import keyring

SERVICE_NAME = "Forma Studio"
OPENAI_ACCOUNT = "openai_api_key"


def get_key() -> str | None:
    """讀取已儲存的 OpenAI API Key；未設定或 backend 不可用回 None。"""
    try:
        value = keyring.get_password(SERVICE_NAME, OPENAI_ACCOUNT)
    except keyring.errors.KeyringError:
        # keyring backend 不可用（無 GUI、權限被拒、某些 CI 環境）→ 視為未設定
        return None
    return value.strip() if value else None


def set_key(api_key: str) -> None:
    """寫入 API Key 到系統鑰匙圈；空值 raise ValueError。"""
    api_key = api_key.strip()
    if not api_key:
        raise ValueError("api_key is empty")
    keyring.set_password(SERVICE_NAME, OPENAI_ACCOUNT, api_key)


def clear_key() -> None:
    """從系統鑰匙圈刪除已存的 API Key；不存在不 crash。"""
    try:
        keyring.delete_password(SERVICE_NAME, OPENAI_ACCOUNT)
    except keyring.errors.PasswordDeleteError:
        return
