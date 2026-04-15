# =============================================================
# 🔍 TestRail 智能搜尋字典 (Search Dictionary) - 穩定純淨版
# 邏輯：[關鍵代碼, 繁體, 簡體, 英文, 其他關聯標籤/API Key...]
# =============================================================

SEARCH_DICTIONARY = [
    # --- [login / System] 登入與系統狀態 ---
    ["login", "登入", "登录"],
    ["loginKeep", "用戶保持登入狀態重新整理頁面成功", "用户保持登录状态刷新页面成功", "Login by Keeping Login Status to Refresh", "loginKeep"],
    ["loginPhone", "手機號碼登入成功", "手机号码登录成功", "Login by Phone", "loginPhone"],
    ["loginUname", "使用者名稱登入成功", "用户名登录成功", "Login by Username", "loginUname"],
    ["loginSuc", "登入成功", "登录成功", "Login Successfully", "loginSuc"],
    ["logout", "登出", "登出", "Logout", "logoutOuter"],
    ["resend", "重新發送", "重新发送", "Resend", "resend_text", "resend_text1"],

    # --- [Financial] 財務核心 (存提轉) ---
    ["account", "帳戶", "账户", "帳號", "账号"],
    ["deposit", "存款", "充值", "储值", "儲值"],
    ["Withdrawal", "提款", "提現", "提现", "取款"],
    ["transfer", "轉帳", "轉帳", "Transfer", "劃轉", "划转"],
    ["Wallet", "錢包", "钱包"],
    ["network fee", "網路手續費", "網絡手續費", "gasFee"],
    ["exchange", "閃兌", "閃兌"],
    ["crypto", "虛擬幣", "虛擬貨幣", "加密貨幣", "數字貨幣", "Crypto"],

    # --- [Transaction / Backoffice] 交易日誌與後台操作 ---
    ["trans_log", "交易日誌", "交易日志", "View Transaction Log"],
    ["edit_amount", "編輯到帳金額", "编辑到账金额", "Edit Credited Amount"],
    ["status_check", "狀態查詢和更新", "状态查询和更新", "Status Check"],
    ["callback", "回調商戶", "回调商户", "Callback to Merchant"],
    ["order_cancel", "沖正撤單", "沖正撤單", "Order Cancellation"],
    ["attachments", "附件", "附件", "Check Attachements"],
    ["channel_alloc", "指定渠道", "指定渠道", "Channel Allocation"],
    ["cancel_withdraw", "取消出款", "取消出款", "Withdrawal Cancellation"],
    ["allocated", "更改為已分配", "更改为已分配", "Update to Allocated"],
    ["pending_alloc", "為待分配", "为待分配", "Update to Pending Allocation"],

    # --- [auManage] 權限與成員管理 ---
    ["auManage", "權限管理", "權限管理", "Authority Management", "access", "authority"],
    ["addRole", "新增角色", "新增角色", "Add Role", "roleAdd", "enterName", "roleList"],
    ["addMem", "新增成員", "新增成員", "Add User", "create", "creater", "addMem"],
    ["adSuc", "新增成功", "添加成功", "Successfully Added"],
    ["accRoleAdd", "帳號角色添加成功", "帳號角色添加成功！"],
    ["Group", "所屬群組", "所屬群組"],
    ["changeSuc", "更新成功", "更新成功", "Update Successful"],
    ["resetPassword", "重置密碼", "重置密碼", "Reset Password"],
    ["accManage", "帳號管理", "帳號管理", "Account Management"],

    # --- [Bonus & VIP] 紅利、活動與流水 ---
    ["Bonus wallet", "獎金錢包", "獎金錢包"],
    ["Fragment", "網址片段", "錨點", "錨點"],
    ["Routing", "路由", "跳轉", "跳轉", "導航", "Navigation"],
    ["Deposit Bonus", "存款紅利", "存款紅利"],
    ["bonus_fs", "免費旋轉", "免費旋轉", "Free Spin", "fs"],
    ["bonus_fc", "免費籌碼", "免費籌碼", "Free Chip", "fc"],
    ["turnover", "提款流水要求", "提款流水要求", "Withdrawal To Requirements"],
    ["reward_status", "待領取", "待認領", "Wait to be claimed", "left_claim", "wait_claimed", "remaining_reward_amount", "left_to_claim"],
    ["vip_bene", "保級福利", "保級福利", "Maintenance Bonus", "rege_bene", "retentionBonus", "birthdayBonus", "upgradeLedPackage"],
    ["neg_clear", "負值清零", "負值清零", "Clear negative assets", "c_n_assets", "negativeClear"],
    ["clear_credit", "抵用金清零", "抵用金清零", "Clear credit"],

    # --- [Social] 社交帳號與第三方綁定 ---
    ["Social Account", "社交帳號", "社交賬號", "第三方登錄", "三方登入"],
    ["QQ", "騰訊", "Tencent", "企鵝"],
    ["Telegram", "TG", "電報", "飛機"],
    ["微信", "WeChat", "WX", "Weixin"],
    ["微博", "Weibo", "WB"],

    # --- [KYC & Risk] 認證與風控 ---
    ["kyc", "身分認證", "身份認證", "Identity Verification"],
    ["prof_ad", "地址證明", "地址證明", "Proof of Address", "poa", "residence_ad"],
    ["edd", "風險評估問卷", "風險評估問卷", "Risk Assessment Questionnaire", "edd_veri", "edd_popup_tips", "加強型盡職調查"],
    ["sow", "財富來源", "財富來源", "Source of Wealth", "source_wealth", "proof_wealth"],
    ["face_verify", "活體認證", "活體認證", "Face Verification", "livingBody", "faceRecognition", "vivoAuthentication"],
    ["risk", "風控管理", "風控管理", "Risk Management", "windControl", "riskLevel", "highRiskMemberDetail"],

    # --- [System / UI] 基礎設施與更新 ---
    ["notification", "系統通知", "系統通知", "System Notification", "messageManagement", "insite_noti", "notification"],
    ["report", "報表下載", "報表下載", "Report Download", "reportDownload", "playerPromotion", "vipPerformance", "dailyDataRecon"],
    ["update", "更新", "Update", "new_version_discovered", "update_immediately", "new_version"],
    ["maintenance", "維護中", "維護中", "service_maintain_text1", "game_main", "maintenance"],

    # --- [Fiat] 法幣與傳統支付 ---
    ["fiat", "法幣", "法幣"],
    ["bank_card", "銀行卡", "銀行卡", "金融卡", "Bank Card", "bankCard", "debitCard", "creditCard", "card_number"],
    ["bank_name", "銀行名稱", "Bank Name", "bankName", "branchName", "issuing_bank"],
    ["otc", "場外交易", "OTC", "otc_trade", "p2p_trading", "商家交易"],
    ["payment_gate", "支付通道", "三方支付", "Payment Gateway", "channelName", "merchantId", "payment_method"],
    ["offline_pay", "線下轉帳", "線下匯款", "Offline Transfer", "remittance", "receipt_upload", "上傳憑證"]
]
