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
    """ 
    取得可選路徑清單：
    1. 優先使用從 TestRail API 抓取的清單
    2. 否則依據 env_type (FE, GoGaming, GoMoney) 傳回完整的模組清單
    """
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


def generate_test_outline(summary: str, description: str) -> str:
    prompt = f"請針對以下 Jira 需求，列出測試大綱條目（每行一條重點，不要贅詞）：\n摘要：{summary}\n描述：{description}"
    return call_gemini_with_retry(prompt)


def generate_test_cases(
    summary: str,
    description: str,
    outline: str,
    env_type: str = "GoGaming",
    path_hint: str = None,
    selected_path: str = None,  # 👈 使用者從 UI 手動選取的模組路徑
    available_paths: list = None,
) -> list:
    """
    生成測試案例：
    若 selected_path (或 path_hint) 有指定明確路徑，AI 會強制套用該路徑；
    否則提供系統模組清單供 AI 參考。
    """
    # 決定最終要套用的路徑名稱
    target_path = selected_path or path_hint
    
    # 判斷使用者是否傳入了有效的指定路徑
    has_custom_path = target_path and target_path not in [
        "🤖 [自動由 AI 判斷路徑]",
        "其他",
        "",
        None
    ]

    candidate_paths = get_candidate_paths(env_type, f"{summary} {description} {outline}", available_paths=available_paths)
    paths_str = "\n".join([f"- {p}" for p in candidate_paths])

    if has_custom_path:
        # 使用者手動選定路徑的嚴格 Prompt
        path_instruction = f"""1. path 欄位請固定輸出："{target_path}"
2. steps 内 Step 1 請統一寫為：1. 路徑：{target_path}"""
    else:
        # 讓 AI 從清單中挑選的 Prompt
        path_instruction = f"""1. path 必須「完全相同」地引用以下系統路徑清單中的其中一條：
{paths_str}
2. steps 内 Step 1 請統一寫為：1. 路徑：[選取的 path]"""

    system_prompt = f"""你是一位資深 QA。請分析 Jira 需求與大綱，並將其轉換為 TestRail 測試案例 JSON Array。

【路徑匹配指令】：
{path_instruction}

【案例結構規範】：
- title: [模組]-情境 或 [動作]-目的
- preconditions: 前置條件列表
- steps:
   - content 格式：
     1. 路徑：[對應路徑]
     2. [動作/步驟]
     • [具體測試情境]
   - expected: 預期結果，若有錯誤提示用 Tips Red Error Message :

回傳格式（標準 JSON）：
[
  {{
    "title": "[优惠券管理]-新增优惠券类型选单验证",
    "path": "{target_path if has_custom_path else 'GoGaming > 营销推广 > 优惠券管理'}",
    "preconditions": [
      "1. 登入後台管理系統。",
      "2. 具備優惠券管理權限。"
    ],
    "steps": [
      {{
        "content": "1. 路徑：{target_path if has_custom_path else 'GoGaming > 营销推广 > 优惠券管理'}\\n2. 點擊創建優惠券並檢查類型下拉選單\\n   • 檢查類型選單中是否正確新增選項",
        "expected": "優惠券類型選單正確包含並顯示對應選項。"
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
        
        # 後處理：若使用者手動選定了模組路徑，強制校正所有案例的 path 欄位
        for case in cases:
            if has_custom_path:
                case["path"] = target_path
            elif not case.get("path") or case.get("path") == "其他":
                case["path"] = candidate_paths[0] if candidate_paths else "GoGaming > 营销推广 > 优惠券管理"
                
        return cases
    except json.JSONDecodeError:
        raise CaseGenError("AI 回傳格式非有效 JSON，請再試一次。")
