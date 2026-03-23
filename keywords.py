# keywords.py

# =============================================================
# 🔍 TestRail 智能搜尋字典 (Search Dictionary)
# 邏輯：[關鍵代碼, 繁體, 簡體, 英文, 其他關聯標籤/API Key...]
# =============================================================

SEARCH_DICTIONARY = [
    # --- [login / System] 登入與系統狀態 ---
    ["loginEnter", "登入", "登录", "Login", "login", "loginWay"],
    ["loginKeep", "用戶保持登入狀態重新整理頁面成功", "用户保持登录状态刷新页面成功", "Login by Keeping Login Status to Refresh", "loginKeep"],
    ["loginPhone", "手機號碼登入成功", "手机号码登录成功", "Login by Phone", "loginPhone"],
    ["loginUname", "使用者名稱登入成功", "用户名登录成功", "Login by Username", "loginUname"],
    ["loginSuc", "登入成功", "登录成功", "Login Successfully", "loginSuc"],
    ["logout", "登出", "登出", "Logout", "logoutOuter"],
    ["resend", "重新發送", "重新发送", "Resend", "resend_text", "resend_text1"],

    # --- [Financial] 財務核心 (存提轉) ---
    ["deposit", "存款", "存款", "Deposit", "充值", "充值", "depositList", "recharge", "creditedAmount", "depositRate"],
    ["withdraw", "提款", "提款", "Withdrawal", "提現", "提现", "withdrawList", "withdrawal", "wdAmount", "withdrawalMethod"],
    ["transfer", "轉帳", "转账", "Transfer", "劃轉", "划转", "transferRecord", "transferTime", "fromWalletCategory", "toWalletCategory"],
    ["main_w", "主錢包", "主钱包", "Main Account", "Main Wallet", "masterAccount"],
    ["network_fee", "網路手續費", "网络手续费", "Network fee", "network__fee", "digitalFee", "gasFee"],
    ["exchange", "閃兌", "闪兑", "Rapid Exchange", "conversion", "previewExchange", "transactionOrderNo"],
    ["trans_addr", "轉出地址", "转出地址", "Transfer address", "transAddress", "receiveAddress", "transHash"],

    # --- [auManage] 權限與成員管理 ---
    ["auManage", "權限管理", "权限管理", "Authority Management", "qx", "access", "authority"],
    ["addRole", "新增角色", "新增角色", "Add Role", "roleAdd", "enterName", "roleList"],
    ["addMem", "新增成員", "新增成員", "Add User", "create", "creater", "addMem"],
    ["adSuc", "新增成功", "添加成功", "Successfully Added", "accRoleAdd", "Successfully created", "roleSuc", "accSuc"],
    ["accRoleAdd", "帳號角色添加成功", "账号角色添加成功！", "New Role Is Added", "accRoleAdd"],
    ["beGroup", "所屬群組", "所属群组", "Group", "gName", "gList", "enterNameGroup"],
    ["changeSuc", "更新成功", "更新成功", "Update Successful", "editSuc", "accSourceSuc", "changeSuc"],
    ["resetPassword", "重置密碼", "重置密码", "Reset Password", "passwordSuc", "newPassword", "failedPassword"],
    ["accManage", "帳號管理", "账号管理", "Account Management", "accList", "accountManagement", "sys_acc"],

    # --- [Bonus & VIP] 紅利、活動與流水 ---
    ["bonus_wallet", "獎金錢包", "奖金钱包", "Bonus wallet", "bonusWalletEvent", "bonusWalletAcc"],
    ["Fragment", "碎片", "锚点", "路由", "Routing"],
    ["deposit_bonus", "存款紅利", "存款红利", "Deposit Bonus", "depositBonusEvent", "extraDepositBonus"],
    ["bonus_fs", "免費旋轉", "免费旋转", "Free Spin", "fs", "bonus_fs_tag", "bonus_fs_count", "numberOfSpins", "spin_value", "freeSpinPrize"],
    ["bonus_fc", "免費籌碼", "免费筹码", "Free Chip", "fc", "bonus_fc_tag", "bonus_fc_worth", "numberOfChips", "freeChipPrize"],
    ["turnover", "提款流水要求", "提款流水要求", "Withdrawal To Requirements", "depositLimit", "turnoverMultiple", "wagerRequirement", "bet_process"],
    ["reward_status", "待領取", "待认领", "Wait to be claimed", "left_claim", "wait_claimed", "remaining_reward_amount", "left_to_claim"],
    ["vip_bene", "保級福利", "保级福利", "Maintenance Bonus", "rege_bene", "retentionBonus", "birthdayBonus", "upgradeLedPackage"],
    ["neg_clear", "負值清零", "负值清零", "Clear negative assets", "c_n_assets", "negativeClear"],
    ["clear_credit", "抵用金清零", "抵用金清零", "Clear credit", "confirm_clear_credit_title", "clear_credit_desc1", "clear_credit_desc4"],

    # --- [Social] 社交帳號與第三方綁定 ---
    ["social_acc", "社交帳號", "社交账号", "Social Account", "第三方登錄", "三方登入", "綁定", "绑定", "Bind", "Unbind", "解綁"],
    ["QQ", "騰訊", "Tencent", "企鵝"],
    ["Telegram", "TG", "電報", "飛機"],
    ["微信", "WeChat", "WX", "Weixin"],
    ["微博", "Weibo", "WB"],
    ["Line", "連我", "連賴", "LNE"],
    ["ebpay", "EBPay", "EBPay", "ebpay_ad", "eb_pay", "eb_complete"],

    # --- [KYC & Risk] 認證與風控 ---
    ["kyc", "身分認證", "身份认证", "Identity Verification", "Identification", "kycManagement", "basic_ver", "mid_ver", "ad_ver"],
    ["prof_ad", "地址證明", "地址证明", "Proof of Address", "poa", "residence_ad"],
    ["edd", "風險評估問卷", "風險評估問卷", "Risk Assessment Questionnaire", "edd_veri", "edd_popup_tips", "加強型盡職調查"],
    ["sow", "財富來源", "财富来源", "Source of Wealth", "source_wealth", "proof_wealth"],
    ["face_verify", "活體認證", "活体认证", "Face Verification", "livingBody", "faceRecognition", "vivoAuthentication"],
    ["risk", "風控管理", "风控管理", "Risk Management", "windControl", "riskLevel", "highRiskMemberDetail"],

    # --- [Affiliate] 聯盟計畫 (代理) ---
    ["affiliate", "聯盟計畫", "联盟计划", "Affiliate Program", "global_alli", "affiliate_join_how", "affiliate_step1_title"],
    ["sub_agent", "下級代理", "下级代理", "Sub-agent", "subUID", "fourth_recom"],
    ["aff_comm", "佣金率", "佣金率", "Commission ratio", "commission_ratio", "affiliate_banner_title", "高达55%佣金比例"],

    # --- [System / UI] 基礎設施與更新 ---
    ["notification", "系統通知", "系统通知", "System Notification", "messageManagement", "insite_noti", "notification"],
    ["report", "報表下載", "报表下载", "Report Download", "reportDownload", "playerPromotion", "vipPerformance", "dailyDataRecon"],
    ["update", "更新", "Update", "new_version_discovered", "update_immediately", "new_version"],
    ["maintenance", "維護中", "維護中", "service_maintain_text1", "game_main", "maintenance"]
]
