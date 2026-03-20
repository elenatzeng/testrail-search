# keywords.py

# 🏆 拍檔特製：JSON 檔案全量提取版
# 此字典已根據妳提供的 4 份 JSON (en-US, zh-CN) 進行地毯式補完，
# 包含 loginKeep, 權限管理, TRON能量, 閃兌列表等所有細節。

SEARCH_DICTIONARY = [
    # --- [allPop] 登錄與系統彈窗相關 ---
    ["loginKeep", "用戶保持登錄狀態刷新頁面成功", "用户保持登录状态刷新页面成功", "Login by Keeping Login Status to Refresh"],
    ["loginPhone", "手機號碼登錄成功", "手机号码登录成功", "Login by Phone"],
    ["loginUname", "用戶名登錄成功", "用户名登录成功", "Login by Username"],
    ["loginEnter", "登錄", "登录", "Login"],
    ["loginWay", "登錄方式", "登录方式", "Login Method"],
    ["logoutOuter", "登出", "登出", "Logout"],
    ["login", "登錄成功", "登录成功", "Login Successfully"],
    ["logout", "登錄失敗", "登录失败", "Login Failed"],

    # --- [auManage] 權限與角色管理 (QA 測試重點) ---
    ["auManage", "權限管理", "权限管理", "Authority Management"],
    ["addMem", "新增成員", "新增成员", "Add User"],
    ["addRole", "新增角色", "新增角色", "Add Role"],
    ["beGroup", "所屬群組", "所属群组", "Group"],
    ["collapseAll", "收起所有", "收起所有", "Collapse All"],
    ["enterName", "請輸入搜索角色名稱", "请输入搜索角色名称", "Search for role name"],

    # --- [energy] TRON 能量與補貼 (技術類 Case) ---
    ["energyOnly", "僅能量", "仅能量", "Energy Only"],
    ["trxOnly", "僅TRX", "仅TRX", "TRX Only"],
    ["automatedTopUp", "自動充值配置", "自动充值配置", "Automated Top Up Configuration"],
    ["targetAmount", "目標金額", "目标金额", "Target amount"],

    # --- [exchange] 閃兌與兌換列表 ---
    ["transactionOrderNo", "交易所訂單號", "交易所订单号", "Exchange Order Number"],
    ["transAddress", "轉出地址", "转出地址", "Transfer address"],
    ["receiveAddress", "接收地址", "接收地址", "Receiving address"],
    ["transHash", "轉出Hash", "转出Hash", "Transfer out Hash"],
    ["previewExchange", "預覽兌換匯率", "预览兑换汇率", "Preview Exchange Rate"],

    # --- [event / popupBanner] 活動與彈窗 ---
    ["bonusWalletEvent", "獎金錢包活動", "奖金钱包活动", "Bonus Wallet Event"],
    ["depositBonusEvent", "存款紅利活動", "存款红利活动", "Deposit Bonus Event"],
    ["bannerText", "彈窗文案", "弹窗文案", "Popup Banner Text"],
    ["displayPeriod", "展示期間", "展示期间", "Display Period"],

    # --- ✨ 妳指定的特殊 Bonus 類型 (嚴格獨立) ---
    ["bonus_fs_tag", "免費旋轉", "免费旋转", "Free Spin", "fs"],
    ["bonus_fc_tag", "免費籌碼", "免费筹码", "Free Chip", "fc"],
    ["bonus_fs_count", "免費旋轉次數", "免费旋转次数", "Free Spin Count"],
    ["bonus_fc_worth", "免費籌碼總值", "免费筹码总值", "Free Chip Worth"],
    ["spin_value", "旋轉單價", "旋转单价", "Spin Value"],

    # --- 錢包與支付支付 (依據最新 JSON 補全) ---
    ["main_w", "主錢包", "主钱包", "Main Account"],
    ["bonus_wallet", "獎金錢包", "奖金钱包", "Bonus wallet"],
    ["network__fee", "網絡手續費", "网络手续费", "Network fee"],
    ["ebpay", "EBPay", "eb_pay", "ebpay_ad"],
    ["koi_pay", "KOIPay", "koi_pay"],
    ["clear_credit", "抵用金清零", "Clear credit"],
    ["confirm_clear_credit_title", "抵用金清零提醒", "Clear credit reminder"],
    ["edd_veri", "EDD驗證", "EDD验证", "EDD Verification"],
    ["source_wealth", "財富來源", "财富来源", "Source of Wealth"],

    # --- 體育與盤口 (細項) ---
    ["ob_handicap_name_1", "全場獨贏", "全场独赢", "Match Winner"],
    ["correct_score", "波膽", "波胆", "Correct Score"],
    ["handicap", "讓球", "让球", "Handicap"]
]
