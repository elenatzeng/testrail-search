import json
import re
import google.generativeai as genai

# --- 根據截圖精準提取的三端 (前台/GoGaming/GoMoney) 固定功能路徑樹 ---
SYSTEM_PATH_TREE = """
【前台功能目錄 (精簡版)】
- 前台 > 首页 > 我的钱包 > 钱包总览 > 充值
- 前台 > 首页 > 我的钱包 > 钱包总览 > 提现
- 前台 > 首页 > 我的钱包 > 钱包总览 > 劃轉
- 前台 > 首页 > 我的钱包 > 钱包总览 > 钱包历史记录
- 前台 > 首页 > 我的钱包 > 银行卡管理
- 前台 > 首页 > 我的钱包 > 支付宝管理
- 前台 > 首页 > 我的钱包 > 数字货币地址管理
- 前台 > 首页 > 我的钱包 > 钱包历史记录
- 前台 > 首页 > 订单 > 体育订单
- 前台 > 首页 > 订单 > 彩票订单
- 前台 > 首页 > 订单 > 娱乐城订单
- 前台 > 首页 > 订单 > 棋牌订单
- 前台 > 首页 > 头像功能列 > 个人中心
- 前台 > 首页 > 头像功能列 > 奖金中心
- 前台 > 首页 > 头像功能列 > 社交媒体(注册、登录)
- 前台 > 首页 > 头像功能列 > 偏好设置
- 前台 > 首页 > 头像功能列 > 账户安全
- 前台 > 首页 > 头像功能列 > 通知
- 前台 > 首页 > 头像功能列 > 下载
- 前台 > 首页 > 导航栏
- 前台 > 首页 > 首页Banner
- 前台 > 侧栏功能 > 最新优惠 > 全部
- 前台 > 侧栏功能 > 最新优惠 > 新用户专享
- 前台 > 侧栏功能 > 最新优惠 > 常规活动
- 前台 > 侧栏功能 > 最新优惠 > 限时活动
- 前台 > 侧栏功能 > 我的收藏
- 前台 > 侧栏功能 > 近期所有玩过的
- 前台 > 侧栏功能 > 游戏
- 前台 > 侧栏功能 > 在线客服
- 前台 > 侧栏功能 > 语言
- 前台 > 侧栏功能 > 日夜间版

【GoGaming 後台功能目錄】
- GoGaming > 仪表盘
- GoGaming > 会员管理 > 会员列表
- GoGaming > 会员管理 > VIP管理
- GoGaming > 会员管理 > VIP红利管理
- GoGaming > 会员管理 > KYC管理
- GoGaming > 营销推广 > 仪表盘
- GoGaming > 营销推广 > 代理列表
- GoGaming > 营销推广 > 待审核列表
- GoGaming > 营销推广 > 佣金审核列表
- GoGaming > 营销推广 > 订阅列表
- GoGaming > 营销推广 > 活动管理
- GoGaming > 营销推广 > 发放查询
- GoGaming > 营销推广 > 奖品管理
- GoGaming > 营销推广 > 优惠券管理
- GoGaming > 营销推广 > 推荐好友
- GoGaming > 财务管理 > 入款记录
- GoGaming > 财务管理 > 提款审核
- GoGaming > 财务管理 > 调账记录
- GoGaming > 财务管理 > 转账记录
- GoGaming > 财务管理 > 代客充值
- GoGaming > 财务管理 > 提款审核配置
- GoGaming > 财务管理 > 獎金錢包資金紀錄
- GoGaming > 支付管理 > 币种配置
- GoGaming > 支付管理 > 支付方式管理
- GoGaming > 支付管理 > 提款信息绑定管理
- GoGaming > 游戏管理 > 厂商管理
- GoGaming > 游戏管理 > 游戏管理
- GoGaming > 游戏管理 > 标签管理
- GoGaming > 游戏管理 > 交易记录(New)
- GoGaming > 游戏管理 > 交易记录
- GoGaming > 游戏管理 > 交易统计
- GoGaming > 游戏管理 > 第三方游戏管理
- GoGaming > 游戏中心 > 游戏串接
- GoGaming > 游戏中心 > 交易记录
- GoGaming > 原创管理 > 注单查询
- GoGaming > 原创管理 > 限额设定
- GoGaming > 原创管理 > 输赢分析
- GoGaming > 原创管理 > 盈利率分析
- GoGaming > 风控管理 > IP监控
- GoGaming > 风控管理 > 实时监控列表
- GoGaming > 风控管理 > 自动审核记录
- GoGaming > 风控管理 > 风控规则配置
- GoGaming > 风控管理 > 待补充列表
- GoGaming > 风控管理 > 批量操作
- GoGaming > 风控管理 > 批量状态
- GoGaming > 风控管理 > 资金流向分析
- GoGaming > 风控管理 > 最优胜报表
- GoGaming > 风控管理 > 不良数据
- GoGaming > 风控管理 > 设备指纹
- GoGaming > 风控管理 > 钱包地址 Crypto Address
- GoGaming > 内容管理 > 资讯分类管理
- GoGaming > 内容管理 > 资讯管理
- GoGaming > 内容管理 > 弹窗Banner
- GoGaming > 内容管理 > Banner管理
- GoGaming > 内容管理 > 页尾管理
- GoGaming > 内容管理 > 司法管辖区配置
- GoGaming > 内容管理 > 多语言配置
- GoGaming > 内容管理 > 站内信管理
- GoGaming > 消息管理 > 在线消息历史记录
- GoGaming > 消息管理 > 对话
- GoGaming > 消息管理 > 自动回复管理 Away Message Management
- GoGaming > 消息管理 > 主题管理
- GoGaming > 消息管理 > Comm100 历史聊天
- GoGaming > 权限管理 > 系统账号管理
- GoGaming > 权限管理 > 角色管理
- GoGaming > 权限管理 > 群组管理
- GoGaming > 系统管理 > 市场管理
- GoGaming > 系统管理 > 商户管理
- GoGaming > 系统管理 > 操作日志
- GoGaming > 实用工具 > OTP查询
- GoGaming > 实用工具 > 红利图片上传
- GoGaming > 实用工具 > 手机查询
- GoGaming > 实用工具 > 数据统计
- GoGaming > 实用工具 > VIP報表
- GoGaming > 实用工具 > SMS & Email查詢
- GoGaming > 实用工具 > 更新會員註冊渠道碼
- GoGaming > 实用工具 > 代理轉移
- GoGaming > 实用工具 > 數據導出
- GoGaming > 实用工具 > 報告查看
- GoGaming > 实用工具 > 離線下載
- GoGaming > 实用工具 > NGR報表

【GoMoney 後台功能目錄】
- GoMoney > 首页
- GoMoney > 会员管理
- GoMoney > 财务管理 > 付款申请
- GoMoney > 财务管理 > 付款审批
- GoMoney > 财务管理 > 存款列表
- GoMoney > 财务管理 > 提款列表
- GoMoney > 财务管理 > 調帳列表
- GoMoney > 财务管理 > 換匯列表
- GoMoney > 财务管理 > 所有交易
- GoMoney > 财务管理 > 交易列表 2.0
- GoMoney > 财务管理 > Gas費報告
- GoMoney > 财务管理 > 财务管理
- GoMoney > 财务管理 > 虚拟货币存提速度优化
- GoMoney > 支付管理 > 币种配置
- GoMoney > 支付管理 > 支付方式配置
- GoMoney > 支付管理 > 商户支付方式配置
- GoMoney > 支付管理 > 法币渠道配置
- GoMoney > 支付管理 > 法币子渠道配置
- GoMoney > 支付管理 > 渠道配置2.0
- GoMoney > 支付管理 > 渠道分配管理
- GoMoney > 支付管理 > 公司帐户管理
- GoMoney > 支付管理 > 汇率管理
- GoMoney > 支付管理 > 银行列表配置
- GoMoney > 支付管理 > 银行映射配置
- GoMoney > 支付管理 > PSP分配设置
- GoMoney > 支付管理 > 提款审核配置
- GoMoney > 支付管理 > VIP PSP分配
- GoMoney > 支付管理 > 兑换记录
- GoMoney > 财务钱包
- GoMoney > 钱包管理 > 冷钱包
- GoMoney > 钱包管理 > 用户钱包
- GoMoney > 钱包管理 > 热钱包
- GoMoney > 钱包管理 > 闪兑Flash Swap
- GoMoney > 钱包管理 > TRON NETWORK
- GoMoney > 风控管理
- GoMoney > 报表 > GBPay-商户热钱包对账表
- GoMoney > 报表 > GBPay-玩家热钱包对账表
- GoMoney > 报表 > 法币PSP对账表
- GoMoney > 报表 > 虚拟币PSP对账表
- GoMoney > 权限管理 > 系统账号管理
- GoMoney > 权限管理 > 角色管理
- GoMoney > 系统管理 > 组织管理
- GoMoney > 系统管理 > 操作日志
- GoMoney > 系统管理 > 商户IP白名单
- GoMoney > 实用工具 > 报告查看
"""

SYSTEM_PROMPT = f"""
你是一位資深 QA 與 UI 自動化測試專家。請將輸入的需求或大綱，轉換為極簡、精準、結構化的 TestRail 測試案例（JSON 格式）。

請嚴格遵守以下【標題與路徑規範】：

1. Path (功能路徑規範 - 僅允許功能層級)：
   - **必須且只能**完全匹配以下【固定功能路徑清單】中的其中一條，絕不可自行延伸階層或加上細項目錄：
{SYSTEM_PATH_TREE}

2. Title (標題命名規範)：
   - 格式 1（檢核類）：`[模組/類別] - [具體情境]`
     範例：`共用檢核 - 輸入範圍外的提款金額`、`數字貨幣檢核 - 提幣地址錯誤`
   - 格式 2（流程/動作類）：`[動作/步驟名稱] - [目的/動作對象]`
     範例：`点击[确认] - 送出提现单`、`提现信息 - 提款至 / Withdrawal to`

3. Steps Content (操作步驟 - 必須含路徑第 1 點)：
   - 第 1 點必須強制帶入：`1. 路徑：[選取的指定功能路徑]`
   - 步驟使用極簡動詞開頭，絕不寫「請」、「確認」等贅詞。
   - 主要步驟用數字（2., 3.），具體測試輸入情境用 Bullet point（•）。
   - 範例：
     1. 路徑：前台 > 首页 > 我的钱包 > 钱包总览 > 提现
     2. 选择支付方式
     3. 输入提款金额
        • 请输入大于范围外数字
        • 请输入小于范围的数字

4. Steps Expected (預期結果與提示訊息)：
   - 錯誤提示需明確標註，如 `Tips Red Error Message :`。
   - 若涉及多語系或前後對比，請條列呈現（CN / EN 或 變更前 / 變更後）。
   - 範例：
     Tips Red Error Message :
     • CN : 提现金额必须介于 n - m {{Currency}}之间。
     • EN : Withdrawal amount must be between n - m {{Currency}}

--------------------------------------------------
JSON 輸出格式約束（請直接輸出標準 JSON Array）：
[
  {{
    "title": "提现信息 - 请输入金额 (币别) / Enter Amount (Currency)",
    "path": "前台 > 首页 > 我的钱包 > 钱包总览 > 提现",
    "preconditions": [
      "1. 當前登入帳號已成功登入系統並具備提現權限。"
    ],
    "steps": [
      {{
        "content": "1. 路徑：前台 > 首页 > 我的钱包 > 钱包总览 > 提现\n2. 选择支付方式\n3. 输入提款金额\n   • 请输入大于范围外数字\n   • 请输入小于范围的数字",
        "expected": "Tips Red Error Message :\n• CN : 提现金额必须介于 n - m {{Currency}}之间。\n• EN : Withdrawal amount must be between n - m {{Currency}}"
      }}
    ]
  }}
]
"""

class CaseGenError(Exception):
    pass

def generate_test_outline(summary: str, description: str) -> str:
    """呼叫 Gemini 產生測試大綱"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"請針對以下 Jira 需求，列出測試大綱條目（每行一條重點，不要贅詞）：\n摘要：{summary}\n描述：{description}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise CaseGenError(f"產生大綱失敗：{str(e)}")

def generate_test_cases(summary: str, description: str, outline: str, path_hint: str = None) -> list:
    """呼叫 Gemini 產生極簡風格與固定路徑的 Test Cases"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        user_input = f"Jira 摘要：{summary}\nJira 描述：{description}\n測試大綱：\n{outline}"
        if path_hint:
            user_input += f"\n使用者指定優先路徑：{path_hint}"

        response = model.generate_content([SYSTEM_PROMPT, user_input])
        raw_text = response.text.strip()

        # 清除 Markdown 程式碼區塊標記
        cleaned_text = re.sub(r"^```json\s*", "", raw_text, flags=re.MULTILINE)
        cleaned_text = re.sub(r"^```\s*", "", cleaned_text, flags=re.MULTILINE).strip()

        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        raise CaseGenError("AI 回傳的格式非有效 JSON，請再試一次。")
    except Exception as e:
        raise CaseGenError(f"產生測試案例失敗：{str(e)}")
