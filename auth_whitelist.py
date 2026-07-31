# auth_whitelist.py
"""
簡易白名單驗證。
只有 ALLOWED_EMAILS 中列出的 email 才能使用「AI 產生測試案例」功能。

⚠️ 若未來要增加人員，直接編輯這個 set 即可，不需要動到主程式。
"""

ALLOWED_EMAILS = {
    "ela@intellianalyze.com",
    "kh@intellianalyze.com",
}


def is_authorized(email: str) -> bool:
    if not email:
        return False
    return email.strip().lower() in ALLOWED_EMAILS
