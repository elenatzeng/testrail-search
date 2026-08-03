import json
import os
import re
import time

import google.generativeai as genai

SYSTEM_PATHS = {
    "FE": [
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

GEMINI_MODEL_NAME = "gemini-3.6-flash"


class CaseGenError(Exception):
    pass


def _configure_genai() -> None:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GEMINI_API_KEY", "") or st.secrets.get("GOOGLE_API_KEY", "")
        except Exception:
            pass
    if not key:
        raise CaseGenError("找不到 GEMINI_API_KEY，請在 .streamlit/secrets.toml 或環境變數中設定。")
    genai.configure(api_key=key)


def get_candidate_paths(env_type: str, text_content: str, available_paths: list = None) -> list:
    if available_paths and len(available_paths) > 0:
        return available_paths

    paths = SYSTEM_PATHS.get(env_type, [])
    if not paths:
        paths = [p for ps in SYSTEM_PATHS.values() for p in ps]
    return paths


def call_gemini_with_retry(prompt_data, max_retries=4):
    _configure_genai()
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt_data)
            return response.text.strip()
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "quota" in err_msg.lower() or "resourceexhausted" in err_msg.lower().replace("_", ""):
                if attempt < max_retries - 1:
                    time.sleep(4 * (attempt + 1))
                    continue
                else:
                    raise CaseGenError("API 請求過於頻繁（已達免費額度），請等待約 20 秒後再試。")
            elif "404" in err_msg or "not found" in err_msg.lower() or "no longer available" in err_msg.lower():
                raise CaseGenError(
                    f"模型「{GEMINI_MODEL_NAME}」不可用。\n原始錯誤：{err_msg[:300]}"
                )
            else:
                raise CaseGenError(f"API 呼叫失敗：{err_msg}")


# 🧠 1. 大綱層級加強：要求生成業務邏輯與異常規則
def generate_test_outline(summary: str, description: str) -> str:
    prompt = f"""你是一位嚴謹的 Senior QA Lead。請分析以下 Jira 需求，列出完整的測試重點大綱。

【強制覆蓋要求】：
1. 嚴禁只列出 UI/介面佈局測試。
2. 必須包含 **業務邏輯（Business Logic）**：例如金額限制、次數上限、狀態變更流轉、重複領取/操作防禦。
3. 必須包含 **邊界與異常測試（Boundary & Negative Cases）**：例如無權限操作、重複送出、極值驗證、系統失敗時的回滾機制。
4. 必須包含 **前後台數據一致性與資料庫/日誌（Data Integrity）**：例如前台異動後台狀態是否即時更新、操作日誌記錄。

Jira 摘要：{summary}
Jira 描述：{description}

請輸出點條式大綱（每行一個重點，並在開頭標註 [UI/介面]、[業務邏輯]、[異常/邊界] 或 [數據/狀態]）："""
    return call_gemini_with_retry(prompt)


# 🧠 2. 案例生成層級加強：強制深度邏輯步驟
def generate_test_cases(
    summary: str,
    description: str,
    outline: str,
    env_type: str = "GoGaming",
    path_hint: str = None,
    selected_path: str = None,
    available_paths: list = None,
) -> list:
    target_path = selected_path or path_hint

    has_custom_path = target_path and target_path not in [
        "🤖 [自動由 AI 判斷路徑]",
        "其他",
        "",
        None
    ]

    candidate_paths = get_candidate_paths(env_type, f"{summary} {description} {outline}", available_paths=available_paths)
    paths_str = "\n".join([f"- {p}" for p in candidate_paths])

    display_path = target_path if has_custom_path else (candidate_paths[0] if candidate_paths else "GoGaming > 营销推广 > 优惠券管理")

    if has_custom_path:
        path_instruction = f"""1. path 欄位請固定輸出："{target_path}"
2. steps 内 Step 1 的 content 請固定輸出：路徑：{target_path}"""
    else:
        path_instruction = f"""1. path 必須「完全相同」地引用以下系統路徑清單中的其中一條：
{paths_str}
2. steps 内 Step 1 的 content 請輸出：路徑：[選取的 path]"""

    system_prompt = f"""你是一位資深 QA 工程師。請根據 Jira 需求與大綱，生成深度、高質量的測試案例 JSON Array。

【路徑與 Step 拆分關鍵指令】：
{path_instruction}

【測試邏輯深度要求（極度重要）】：
1. **拒絕淺層 UI 案例**：不要只寫「點擊選單」、「欄位顯示」。必須涵蓋 **狀態變更、業務規則、限制觸發、邊界條件、異常覆蓋**。
2. **Step 結構必須拆分為多個獨立物件 (2~4 個 Step)**：
   - **Step 1 (固定導航路徑)**：
     - content: "路徑：{display_path}"
     - expected: "成功進入 {display_path} 頁面。"
   - **Step 2 (核心操作與條件建構)**：
     - content: 具體操作（包含輸入特定數值、重複觸發、權限切換或條件組合）。
     - expected: 頁面反應與前端即時校驗。
   - **Step 3 (業務邏輯與狀態驗證)**：
     - content: 觸發提交、發放、審核，或在另一端（前台/後台）檢查數據。
     - expected: 驗證狀態碼、資料庫變更、次數扣減、金額計算，若有錯誤提示用 Tips Red Error Message :

【案例結構規範】：
- title: [模組]-情境 或 [動作]-目的
- preconditions: 前置條件列表（不要包含任何序號前綴如 "1. "，需標明帳號權限或初始化數據）
- steps: 包含多個 Step 物件的 List

回傳格式（標準 JSON）：
[
  {{
    "title": "[优惠券管理]-重复领取优惠券逻辑与限制校验",
    "path": "{display_path}",
    "preconditions": [
      "玩家帳號已註冊且狀態為正常。",
      "後台已配置限制每人僅可領取 1 次的優惠券。"
    ],
    "steps": [
      {{
        "content": "路徑：{display_path}",
        "expected": "成功進入優惠券管理頁面。"
      }},
      {{
        "content": "使用玩家帳號第一次輸入優惠券代碼並點擊「領取」。",
        "expected": "領取成功，優惠券狀態更新為「已使用」，玩家錢包增加對應紅利。"
      }},
      {{
        "content": "再次輸入相同優惠券代碼並試圖二次領取。",
        "expected": "系統阻擋領取，並彈出提示 Tips Red Error Message : 该优惠券已使用，请勿重复领取，且錢包餘額與數據無異常變動。"
      }}
    ]
  }}
]"""

    user_input = f"Jira 摘要：{summary}\nJira 描述：{description}\n測試大綱：\n{outline}"
    if has_custom_path:
        user_input += f"\n【使用者指定模組/路徑】：{target_path}"

    raw_text = call_gemini_with_retry([system_prompt, user_input])

    cleaned_text = re.sub(r"^```json\s*", "", raw_text, flags=re.MULTILINE)
    cleaned_text = re.sub(r"^```\s*", "", cleaned_text, flags=re.MULTILINE).strip()

    try:
        cases = json.loads(cleaned_text)

        # 後處理：1. 強制校正 path 2. 校正 Step 1 內文 3. 清理 preconditions 前綴數字
        for case in cases:
            if has_custom_path:
                case["path"] = target_path
            elif not case.get("path") or case.get("path") == "其他":
                case["path"] = candidate_paths[0] if candidate_paths else "GoGaming > 营销推广 > 优惠券管理"

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
