# keywords.py

# 🏆 前後台翻譯精準對齊版 - 嚴格按照 JSON 鍵值對應，提供繁/簡/英三語聯想
# 包含：特殊紅利清零、EDD 財富證明、BW 獎金錢包、聯盟計畫細則
SEARCH_DICTIONARY = [
    # --- 1. 基礎登錄與帳號安全性 ---
    ["登入", "登录", "login", "auth", "sign in", "quick login"],
    ["註冊", "注册", "register", "signup", "create user", "join now"],
    ["帳號", "账号", "account", "user", "uid", "username"],
    ["密碼", "密码", "password", "pwd", "initial password"],
    ["驗證碼", "验证码", "verification code", "captcha", "code", "sms code", "email code"],
    ["找回密碼", "找回密码", "retrieve password", "forgot password"],

    # --- 2. 特殊 Bonus 獎勵 (妳指定的特殊類型) ---
    ["免費旋轉", "免费旋转", "free spin", "fs", "bonus_fs_count", "spin_value"],
    ["免費籌碼", "免费筹码", "free chip", "fc", "bonus_fc_worth"],
    ["現金券", "现金券", "cash coupons", "bw_cash", "vouchers"],
    ["存款紅利", "存款红利", "deposit bonus", "home_dp_sub_tit"],
    ["晉級紅利", "晋级红利", "promotion bonus", "pro_bene"],
    ["生日紅利", "生日红利", "birthday bonus", "birthday gift"],
    ["保級福利", "保级福利", "maintenance bonus", "rege_bene"],
    ["救援金", "救援金", "rescue money", "loss relief"],
    ["返水", "返水", "rakeback", "rebate", "return", "estimated_rakeback"],
    ["流水要求", "流水要求", "turnover", "wagering", "requirement", "bet_process"],

    # --- 3. 錢包與支付 (包含清零提醒與錢包細項) ---
    ["存款", "存款", "deposit", "recharge", "topup", "add funds"],
    ["提現", "提现", "withdraw", "withdrawal", "payout", "widthdraw_address"],
    ["主錢包", "主钱包", "main wallet", "main_w"],
    ["獎金錢包", "奖金钱包", "bonus wallet", "bonus_wallet"],
    ["抵用金", "抵用金", "credit", "voucher", "coupon", "credit_consum"],
    ["負值清零", "负值清零", "clear negative assets", "c_n_assets"],
    ["抵用金清零", "抵用金清零", "clear credit", "confirm_clear_credit_title"],
    ["手續費", "手续费", "fee", "network fee", "overhead fee", "gas fee"],
    ["支付寶", "支付宝", "alipay", "ali_bonus", "ali_pay"],
    ["微信支付", "微信支付", "wechat pay", "vx", "vx_guide"],
    ["銀行卡", "银行卡", "bank card", "visa", "mastercard", "bank_acc"],
    ["EBPay", "EBPay", "eb_pay", "ebpay_ad"],
    ["KOIPay", "KOIPay", "koi_pay"],

    # --- 4. 遊戲分類與術語 (嚴格按照供應商翻譯) ---
    ["體育", "体育", "sports", "soccer", "basketball", "lt_sport", "im_sport", "fb_sport"],
    ["電競", "电竞", "esports", "tf_esport", "im_esport", "rg_esport", "ap_esport"],
    ["真人", "真人", "live casino", "ag_live", "bbin_live", "gpi_live", "sa_live"],
    ["棋牌", "棋牌", "chess", "poker", "ky_chess", "yy_chess", "boya_chess", "golden_chess"],
    ["彩票", "彩票", "lottery", "lotto", "ssc", "pk10", "gpi_lottery", "vr_lottery"],
    ["老虎機", "老虎机", "slots", "slot game", "jdb", "ag_slot", "pg_slot"],
    ["捕魚", "捕鱼", "fishing", "fchunter", "kf_fishing"],
    ["盤口術語", "波胆", "correct score", "1x2", "handicap", "odds", "bet option"],
    ["一飛沖天", "一飞冲天", "crash", "o_b_crash"],

    # --- 5. 安全、認證與 EDD 財富來源 ---
    ["身份認證", "身份认证", "kyc", "identification", "verification"],
    ["初級認證", "初级认证", "primary verification", "basic_ver"],
    ["中級認證", "中级认证", "intermediate verification", "mid_ver"],
    ["高級認證", "高级认证", "advanced verification", "ad_ver"],
    ["活體認證", "活体认证", "alive verify", "face_verify", "liveness"],
    ["地址證明", "地址证明", "proof of address", "prof_ad", "utility bill"],
    ["財富證明", "财富证明", "proof of wealth", "source_wealth", "edd_veri"],
    ["企業所有權", "企业所有权", "ownership of a business", "ownership"],
    ["薪資證明", "薪资证明", "salary document", "salary_a_tips"],
    ["谷歌驗證", "谷歌验证", "google authenticator", "2fa", "google_auth"],
    ["手機驗證", "手机验证", "phone verification", "sms_verify", "voice_veri"],

    # --- 6. 聯盟計畫與推薦 ---
    ["聯盟計畫", "联盟计划", "affiliate program", "global_alli"],
    ["代理類型", "代理类型", "agent type", "agent_type"],
    ["佣金比例", "佣金比例", "commission rate", "affiliate_banner_title"],
    ["下級會員", "下级会员", "sub-agent", "sub_agent", "degrade_uid"],
    ["推廣鏈接", "推广链接", "referral link", "rec_link", "refer_links"],

    # --- 7. 系統、UI 與 錯誤訊息 ---
    ["通知", "通知", "notification", "message", "insite_noti", "inbox"],
    ["設定", "设置", "settings", "preference", "config", "global_setting"],
    ["客服", "客服", "customer service", "cs", "online_cs", "live_chat"],
    ["維護", "维护", "maintenance", "in_maint", "game_main"],
    ["更新", "更新", "update", "version", "new_version"],
    ["反饋", "反馈", "feedback", "suggestion", "slow_icon_desc_t"]
]
