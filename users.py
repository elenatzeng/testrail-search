# users.py

# =============================================================
# 👤 使用者管理配置中心 (User Management Center)
# name: 顯示名稱
# weight: 搜尋權重 (建議核心人員 70, 一般 20~40, 離職 5)
# is_active: True (綠標-在職) / False (灰標-離職)
# =============================================================

USER_CONFIG = {
    2:  {"name": "Elena",  "weight": 5, "is_active": True},
    11: {"name": "Katty",  "weight": 5, "is_active": True},
    3:  {"name": "Esther", "weight": 10, "is_active": True},
    4:  {"name": "Emma",   "weight": 10, "is_active": True},
    8:  {"name": "Cooper", "weight": 50, "is_active": True},
    5:  {"name": "Baron",  "weight": 70, "is_active": True},
    6:  {"name": "Meh",    "weight": 5,  "is_active": False}  # ⚪ 標記為 False 自動變灰標
}

# 針對未在名單上的 ID (Other) 的預設配置
DEFAULT_CONFIG = {"name": "Other", "weight": 0, "is_active": True}
