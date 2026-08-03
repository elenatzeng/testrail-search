import json
import re
import time
import google.generativeai as genai
import streamlit as st

# --- 1. SYSTEM_PATHS 完整系統模組地圖（最新正確架構） ---
SYSTEM_PATHS = {
    "WEB": [
        "前台 > 首页 > 我的钱包 > 钱包总览 > 充值",
        "前台 > 首页 > 我的钱包 > 钱包总览 > 提现",
        "前台 > 首页 > 我的钱包 > 钱包总览 > 劃轉",
        "前台 > 首页 > 我的钱包 > 钱包历史记录",
        "前台 > 首页 > 我的钱包 > 银行卡管理",
        "前台 > 首页 > 我的钱包 > 支付宝管理",
        "前台 > 首页 > 我的钱包 > 数字货币地址管理",
        "前台 > 首页 > 订单 > 体育订单",
        "前台 > 首页 > 订单 > 彩票订单",
        "前台 > 首页 > 订单 > 娱乐城订单",
        "前台 > 首页 > 订单 > 棋牌订单",
        "前台 > 首页 > 头像功能列 > 个人中心",
        "前台 > 首页 > 头像功能列 > 奖金中心",
        "前台 > 首页 > 头像功能列 > 社交媒体(注册、登录)",
        "前台 > 首页 > 头像功能列 > 偏好设置",
        "前台 > 首页 > 头像功能列 > 账户安全",
        "前台 > 首页 > 头像功能列 > 通知",
        "前台 > 首页 > 头像功能列 > 下载",
        "前台 > 首页 > 导航栏",
        "前台 > 首页 > 首页Banner",
        "前台 > 侧栏功能 > 最新优惠 > 全部",
        "前台 > 侧栏功能 > 最新优惠 > 新用户专享",
        "前台 > 侧栏功能 > 最新优惠 > 常规活动",
        "前台 > 侧栏功能 > 最新优惠 > 限时活动",
        "前台 > 侧栏功能 > 我的收藏",
        "前台 > 侧栏功能 > 近期所有玩过的",
        "前台 > 侧栏功能 > 游戏",
        "前台 > 侧栏功能 > 在线客服",
        "前台 > 侧栏功能 > 语言",
        "前台 > 侧栏功能 > 日夜间版",
    ],
    "GoGaming": [
        "GoGaming > 仪表盘",
        "GoGaming > 会员管理 > 会员列表",
        "GoGaming > 会员管理 > VIP管理",
        "GoGaming > 会员管理 > VIP红利管理",
        "GoGaming > 会员管理 > KYC管理",
        "GoGaming > 营销推广 > 仪表盘",
        "GoGaming > 营销推广 > 代理列表",
        "GoGaming > 营销推广 > 待审核列表",
        "GoGaming > 营销推广 > 佣金审核列表",
        "GoGaming > 营销推广 > 订阅列表",
        "GoGaming > 营销推广 > 活动管理",
        "GoGaming > 营销推广 > 发放查询",
        "GoGaming > 营销推广 > 奖品管理",
        "GoGaming > 营销推广 > 优惠券管理",
        "GoGaming > 营销推广 > 推荐好友",
        "GoGaming > 财务管理 > 入款记录",
        "GoGaming > 财务管理 > 提款审核",
        "GoGaming > 财务管理 > 调账记录",
        "GoGaming > 财务管理 > 转账记录",
        "GoGaming > 财务管理 > 代客充值",
        "GoGaming > 财务管理 > 提款审核配置",
        "GoGaming > 财务管理 > 獎金錢包資金紀錄",
        "GoGaming > 支付管理 > 币种配置",
        "GoGaming > 支付管理 > 支付方式管理",
        "GoGaming > 支付管理 > 提款信息绑定管理",
        "GoGaming > 游戏管理 > 厂商管理",
        "GoGaming > 游戏管理 > 游戏管理",
        "GoGaming > 游戏管理 > 标签管理",
        "GoGaming > 游戏管理 > 交易记录(New)",
        "GoGaming > 游戏管理 > 交易记录",
        "GoGaming > 游戏管理 > 交易统计",
        "GoGaming > 游戏管理 > 第三方游戏管理",
        "GoGaming > 游戏中心 > 游戏串接",
        "GoGaming > 游戏中心 > 交易记录",
        "GoGaming > 原创管理 > 注单查询",
        "GoGaming > 原创管理 > 限额设定",
        "GoGaming > 原创管理 > 输赢分析",
        "GoGaming > 原创管理 > 盈利率分析",
        "GoGaming > 风控管理 > IP监控",
        "GoGaming > 风控管理 > 实时监控列表",
        "GoGaming > 风控管理 > 自动审核记录",
        "GoGaming > 风控管理 > 风控规则配置",
        "GoGaming > 风控管理 > 待补充列表",
        "GoGaming > 风控管理 > 批量操作",
        "GoGaming > 风控管理 > 批量状态",
        "GoGaming > 风控管理 > 资金流向分析",
        "GoGaming > 风控管理 > 最优胜报表",
        "GoGaming > 风控管理 > 不良数据",
        "GoGaming > 风控管理 > 设备指纹",
        "GoGaming > 风控管理 > 钱包地址 Crypto Address",
        "GoGaming > 内容管理 > 资讯分类管理",
        "GoGaming > 内容管理 > 资讯管理",
        "GoGaming > 内容管理 > 弹窗Banner",
        "GoGaming > 内容管理 > Banner管理",
        "GoGaming > 内容管理 > 页尾管理",
        "GoGaming > 内容管理 > 司法管辖区配置",
        "GoGaming > 内容管理 > 多语言配置",
        "GoGaming > 内容管理 > 站内信管理",
        "GoGaming > 消息管理 > 在线消息历史记录",
        "GoGaming > 消息管理 > 对话",
        "GoGaming > 消息管理 > 自动回复管理 Away Message Management",
        "GoGaming > 消息管理 > 主题管理",
        "GoGaming > 消息管理 > Comm100 历史聊天",
        "GoGaming > 权限管理 > 系统账号管理",
        "GoGaming > 权限管理 > 角色管理",
        "GoGaming > 权限管理 > 群组管理",
        "GoGaming > 系统管理 > 市场管理",
        "GoGaming > 系统管理 > 商户管理",
        "GoGaming > 系统管理 > 操作日志",
        "GoGaming > 实用工具 > OTP查询",
        "GoGaming > 实用工具 > 红利图片上传",
        "GoGaming > 实用工具 > 手机查询",
        "GoGaming > 实用工具 > 数据统计",
        "GoGaming > 实用工具 > VIP報表",
        "GoGaming > 实用工具 > SMS & Email查詢",
        "GoGaming > 实用工具 > 更新會員註冊渠道碼",
        "GoGaming > 实用工具 > 代理轉移",
        "GoGaming > 实用工具 > 數據導出",
        "GoGaming > 实用工具 > 報告查看",
        "GoGaming > 实用工具 > 離線下載",
        "GoGaming > 实用工具 > NGR報表",
    ],
    "GoMoney": [
        "GoMoney > 首页",
        "GoMoney > 会员管理",
        "GoMoney > 财务管理 > 付款申请",
        "GoMoney > 财务管理 > 付款审批",
        "GoMoney > 财务管理 > 存款列表",
        "GoMoney > 财务管理 > 提款列表",
        "GoMoney > 财务管理 > 調帳列表",
        "GoMoney > 财务管理 > 換匯列表",
        "GoMoney > 财务管理 > 所有交易",
        "GoMoney > 财务管理 > 交易列表 2.0",
        "GoMoney > 财务管理 > Gas費報告",
        "GoMoney > 财务管理 > 财务管理",
        "GoMoney > 财务管理 > 虚拟货币存提速度优化",
        "GoMoney > 支付管理 > 币种配置",
        "GoMoney > 支付管理 > 支付方式配置",
        "GoMoney > 支付管理 > 商户支付方式配置",
        "GoMoney > 支付管理 > 法币渠道配置",
        "GoMoney > 支付管理 > 法币子渠道配置",
        "GoMoney > 支付管理 > 渠道配置2.0",
        "GoMoney > 支付管理 > 渠道分配管理",
        "GoMoney > 支付管理 > 公司帐户管理",
        "GoMoney > 支付管理 > 汇率管理",
        "GoMoney > 支付管理 > 银行列表配置",
        "GoMoney > 支付管理 > 银行映射配置",
        "GoMoney > 支付管理 > PSP分配设置",
        "GoMoney > 支付管理 > 提款审核配置",
        "GoMoney > 支付管理 > VIP PSP分配",
        "GoMoney > 支付管理 > 兑换记录",
        "GoMoney > 财务钱包",
        "GoMoney > 钱包管理 > 冷钱包",
        "GoMoney > 钱包管理 > 用户钱包",
        "GoMoney > 钱包管理 > 热钱包",
        "GoMoney > 钱包管理 > 闪兑Flash Swap",
        "GoMoney > 钱包管理 > TRON NETWORK",
        "GoMoney > 风控管理",
        "GoMoney > 报表 > GBPay-商户热钱包对账表",
        "GoMoney > 报表 > GBPay-玩家热钱包对账表",
        "GoMoney > 报表 > 法币PSP对账表",
        "GoMoney > 报表 > 虚拟币PSP对账表",
        "GoMoney > 权限管理 > 系统账号管理",
        "GoMoney > 权限管理 > 角色管理",
        "GoMoney > 系统管理 > 组织管理",
        "GoMoney > 系统管理 > 操作日志",
        "GoMoney > 系统管理 > 商户IP白名单",
        "GoMoney > 实用工具 > 报告查看",
    ],
}


class CaseGenError(Exception):
    """自訂 AI 測試案例產生異常"""
    pass


def get_gemini_model():
    """初始化 Gemini API 模型（最新穩定版）"""
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        raise CaseGenError("未設定 GEMINI_API_KEY，請在 Secrets 中配置。")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-3.6-flash")


def call_gemini_with_retry(prompt_input, max_retries=3, delay=5):
    """帶有自動重試機制的 Gemini 呼叫"""
    model = get_gemini_model()
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt_input,
                generation_config={"temperature": 0.2}
            )
            return response.text
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "ResourceExhausted" in err_str or "Quota" in err_str:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise CaseGenError("API 請求過於頻繁（已達免費額度），請等待約 20 秒後再試。")
            raise CaseGenError(f"Gemini API 呼叫失敗：{e}")


def get_candidate_paths(env_type: str, query_text: str, available_paths: list = None) -> list:
    """計算並排序最合適的系統路徑"""
    paths_to_check = available_paths if available_paths else SYSTEM_PATHS.get(env_type, SYSTEM_PATHS["GoGaming"])
    
    scored_paths = []
    q_words = [w.lower() for w in re.split(r"[\s>_/,\.-]+", query_text) if w]

    for p in paths_to_check:
        score = 0
        p_lower = p.lower()
        for word in q_words:
            if len(word) > 1 and word in p_lower:
                score += 2
        scored_paths.append((score, p))

    scored_paths.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored_paths]


def generate_test_outline(summary: str, description: str) -> str:
    """產生測試大綱"""
    prompt = f"""請分析以下 Jira 需求，列出測試重點大綱：
1. 請包含 [UI/介面]、[業務邏輯]（如狀態流轉/限制）、[異常/邊界] 測試。
2. 每行一條重點，保持精簡。

Jira 摘要：{summary}
Jira 描述：{description}"""
    return call_gemini_with_retry(prompt)


def generate_test_cases(
    summary: str,
    description: str,
    outline: str,
    env_type: str = "GoGaming",
    path_hint: str = None,
    selected_path: str = None,
    available_paths: list = None,
) -> list:
    """產生高品質測試案例"""
    target_path = selected_path or path_hint

    has_custom_path = target_path and target_path not in [
        "🤖 [自動由 AI 判斷路徑]",
        "其他",
        "",
        None
    ]

    candidate_paths = get_candidate_paths(env_type, f"{summary} {description} {outline}", available_paths=available_paths)
    fallback_default = candidate_paths[0] if candidate_paths else SYSTEM_PATHS.get(env_type, ["其他"])[0]
    display_path = target_path if has_custom_path else fallback_default

    # 📌 智能發送機制：指定路徑則直接發送；選 AI 自動判斷時僅提供 Top 20 相關路徑，防止暴 Token
    if has_custom_path:
        path_instruction = f'path 與 Step 1 請固定寫為："路徑：{target_path}"'
    else:
        short_paths = candidate_paths[:20]
        paths_str = "\n".join([f"- {p}" for p in short_paths])
        path_instruction = f"path 請從以下最匹配的路徑中挑選一條：\n{paths_str}"

    system_prompt = f"""你是一位 senior QA。請將 Jira 需求與大綱轉為 TestRail 測試案例 JSON Array。

【核心規則】：
1. {path_instruction}
2. **測試深度**：必須包含 UI 介面、業務邏輯限制（如重複操作阻擋、狀態變更）與異常邊界。
3. **Step 拆分**：必須拆為 2~3 個獨立 Step 物件（Step 1: 進入路徑; Step 2: 操作與輸入; Step 3: 邏輯驗證與預期結果）。
4. Preconditions 不要包含序號（如 1. ）。

JSON 範例：
[
  {{
    "title": "[模組]-情境或邏輯驗證",
    "path": "{display_path}",
    "preconditions": ["前置條件描述"],
    "steps": [
      {{"content": "路徑：{display_path}", "expected": "成功進入頁面"}},
      {{"content": "測試操作與輸入數據", "expected": "畫面與邏輯反應正常"}}
    ]
  }}
]"""

    user_input = f"Jira 摘要：{summary}\n需求描述：{description}\n大綱：\n{outline}"

    raw_text = call_gemini_with_retry([system_prompt, user_input])

    cleaned_text = re.sub(r"^```json\s*", "", raw_text, flags=re.MULTILINE)
    cleaned_text = re.sub(r"^```\s*", "", cleaned_text, flags=re.MULTILINE).strip()

    try:
        cases = json.loads(cleaned_text)

        # 後處理保證路徑精確度
        for case in cases:
            if has_custom_path:
                case["path"] = target_path
            elif not case.get("path") or case.get("path") == "其他":
                case["path"] = fallback_default

            steps = case.get("steps", [])
            if steps and isinstance(steps, list):
                first_step = steps[0]
                content = first_step.get("content", "")

                if "路徑：" in content or "路徑:" in content:
                    new_content = re.sub(r".*?路徑[:：].*?(\n|$)", f"路徑：{case['path']}\n", content)
                    first_step["content"] = new_content.strip()
                else:
                    first_step["content"] = f"路徑：{case['path']}\n" + content

            preconds = case.get("preconditions", [])
            if isinstance(preconds, list):
                case["preconditions"] = [re.sub(r"^\d+[\.\s]*", "", str(p).strip()) for p in preconds]

        return cases
    except json.JSONDecodeError:
        raise CaseGenError("AI 回傳格式非有效 JSON，請再試一次。")
