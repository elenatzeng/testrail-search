# keywords.py

# 🏆 前後台翻譯精準對齊版 - 嚴格按照 JSON 鍵值與前後台翻譯對應
# 包含：特殊紅利 (FS/FC)、EDD 財富證明、錢包清零、系統錯誤碼、各語系 UI 文案
SEARCH_DICTIONARY = [
    # --- 1. 核心與登錄 (含妳抽查的 loginKeep) ---
    ["loginKeep", "用户保持登录状态刷新页面成功", "Login by keeping login status to refresh"],
    ["loginEnter", "登录", "Login"],
    ["loginPhone", "手机号码登录成功", "Login by phone"],
    ["loginUname", "用户名登录成功", "Login by username"],
    ["loginWay", "登录方式", "Login Method"],
    ["logoutOuter", "登出", "Logout"],
    ["auth", "身份驗證", "Authentication"],

    # --- 2. ✨ 特殊獎勵與紅利 (嚴格拆分) ✨ ---
    ["bonus_fs_tag", "免費旋轉", "免费旋转", "Free Spin", "fs"],
    ["bonus_fc_tag", "免費籌碼", "免费筹码", "Free Chip", "fc"],
    ["bonus_fs_count", "免费旋转次数", "Free Spin Count"],
    ["spin_value", "单次旋转价值", "Spin Value"],
    ["bonus_fc_worth", "免费筹码总值", "Free Chip Worth"],
    ["deposit_bonus", "存款红利", "Deposit bonus"],
    ["firstdepositbonus", "首存红利", "First deposit bonus"],
    ["upgradebonus", "升级红包", "Upgrade bonus"],
    ["birthdayBonus", "生日礼金", "Birthday bonus"],
    ["rescue_money", "救援金", "Rescue money"],
    ["rakeback", "返水", "Rakeback", "rebate"],
    ["turnover_requirement", "流水要求", "Turnover Requirement", "wagering"],

    # --- 3. 錢包、支付與清零細項 ---
    ["main_w", "主钱包", "Main Account"],
    ["bonus_wallet", "奖金钱包", "Bonus wallet"],
    ["withdraw", "提现", "Withdrawal"],
    ["deposit", "存款", "Deposit"],
    ["clear_credit", "抵用金清零", "Clear credit"],
    ["confirm_clear_credit_title", "抵用金清零提醒", "Clear credit reminder"],
    ["clear_credit_desc1", "1.抵用金是什么?", "1.What is betting credit?"],
    ["c_n_assets", "负值清零", "Clear negative assets"],
    ["network__fee", "网络手续费", "Network fee"],
    ["bank_card", "银行卡", "Bank card"],
    ["alipay_account", "支付宝账号", "Alipay account"],
    ["ebpay", "EBPay", "eb_pay"],
    ["koi_pay", "KOIPay", "koi_pay"],

    # --- 4. 遊戲供應商與體育 (嚴格按翻譯檔) ---
    ["sports_betting", "体育运动", "Sports Betting"],
    ["esports", "电子竞技", "Esports"],
    ["live_casino", "真人娱乐场", "Live Casino"],
    ["slot_game", "老虎机", "Slot game"],
    ["chess_game", "棋牌", "Chess"],
    ["lottery", "彩票", "Lottery"],
    ["ag_live", "AG真人", "AG Live"],
    ["bbin_live", "BBIN真人", "BBIN Live"],
    ["jdb_desc", "JDB電子", "JDB Slots"],
    ["pingbo", "平博", "Pingbo"],

    # --- 5. 安全、認證與 EDD ---
    ["kyc", "身份认证", "Identity Verification"],
    ["basic_ver", "基础认证", "Basic Verification"],
    ["mid_ver", "中级验证", "Intermediate Verification"],
    ["ad_ver", "高级验证", "Advanced Verification"],
    ["prof_ad", "地址证明", "Proof of Address"],
    ["source_wealth", "财富来源", "Source of Wealth"],
    ["edd_veri", "EDD验证", "EDD Verification"],
    ["face_verify", "活体认证", "Face Verification", "alive verify"],
    ["google_auth", "谷歌验证", "Google Authenticator", "2fa"],

    # --- 6. 聯盟計畫 (Affiliate) ---
    ["affiliate", "联盟计划", "Affiliate Program"],
    ["sub_agent", "下级代理", "Sub-agent"],
    ["commission_ratio", "佣金率", "Commission ratio"],
    ["rec_link", "推广链接", "Referral link"],

    # --- 7. 系統訊息與 UI ---
    ["notification", "系统通知", "System Notification"],
    ["settings", "偏好设置", "Settings"],
    ["customer_service", "客服", "Customer Service", "cs"],
    ["maintenance", "维护中", "Maintenance"],
    ["update", "更新", "Update"],
    ["feedback", "意见和反馈", "Comments and Feedback"]
]
