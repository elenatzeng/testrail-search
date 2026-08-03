import json
import os
import re
import time

import google.generativeai as genai

# --- 將所有目錄精細拆分為列表，方便程式做迴圈尋找 ---

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

# 2026/07 現況：gemini-2.0-flash 已於 2026/6/1 正式關閉下架，呼叫會直接失敗。
# 目前可用的正式版 Flash 模型是 gemini-3.6-flash（比 3.5 便宜、輸出更精簡）。
# Google 汰換模型名稱很頻繁，之後若又收到「模型不存在/no longer available」的錯誤，
# 去 https://ai.google.dev/gemini-api/docs/models 查目前可用的模型 ID 換掉這裡即可。
GEMINI_MODEL_NAME = "gemini-3.6-flash"


class CaseGenError(Exception):
    pass


def _configure_genai() -> None:
    """
    明確設定 API Key，不要依賴 SDK 自動去讀環境變數。
    google.generativeai 預設只會找 GOOGLE_API_KEY 這個環境變數名稱，
    如果 Streamlit secrets 裡設定的是 GEMINI_API_KEY，SDK 不會自動抓到，
    這裡統一從 GEMINI_API_KEY（相容 GOOGLE_API_KEY）讀取，並明確呼叫 configure()。
    """
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GEMINI_API_KEY", "") or st.secrets.get("GOOGLE_API_KEY", "")
        except Exception:
            pass
    if not key:
        raise CaseGenError(
            "找不到 GEMINI_API_KEY，請在 .streamlit/secrets.toml 或環境變數中設定。"
        )
    genai.configure(api_key=key)


def filter_relevant_paths(env_type: str, text_content: str) -> str:
    """ Python 端迴圈尋找：根據需求關鍵字，只過濾出相關的目錄 """
    all_paths = SYSTEM_PATHS.get(env_type, [])
    if not all_paths:
        # 若找不到指定端，自動合併全量目錄
        all_paths = [p for paths in SYSTEM_PATHS.values() for p in paths]

    matched_paths = []
    # 提取需求文案中的所有字詞做關鍵字匹配
    for path in all_paths:
        # 將路徑拆解成小節，如 ["前台", "首页", "我的钱包", "提现"]
        segments = [seg.strip() for seg in path.split(">")]
        # 如果路徑最後幾層關鍵字（如：提现、充值、VIP）有出現在需求文案中
        for seg in segments[1:]:
            if len(seg) >= 2 and seg.lower() in text_content.lower():
                matched_paths.append(path)
                break

    # 如果關鍵字比對不到（例如寫得太抽象），就回傳該端的所有目錄備用
    if not matched_paths:
        matched_paths = all_paths

    # 組合成條列式字串
    return "\n".join([f"- {p}" for p in matched_paths])


def call_gemini_with_retry(prompt_data, max_retries=4):
    """呼叫 Gemini API 封裝（自動重試）"""
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
                    f"模型「{GEMINI_MODEL_NAME}」已不可用（Google 經常汰換模型名稱）。"
                    f"請到 https://ai.google.dev/gemini-api/docs/models 查目前可用的模型 ID，"
                    f"更新 case_generator.py 裡的 GEMINI_MODEL_NAME 常數即可。\n原始錯誤：{err_msg[:300]}"
                )
            else:
                raise CaseGenError(f"API 呼叫失敗：{err_msg}")


def generate_test_outline(summary: str, description: str) -> str:
    """產生測試大綱（極簡 Prompt）"""
    prompt = f"請針對以下 Jira 需求，列出測試大綱條目（每行一條重點，不要贅詞）：\n摘要：{summary}\n描述：{description}"
    return call_gemini_with_retry(prompt)


def generate_test_cases(summary: str, description: str, outline: str, env_type: str = "GoGaming", path_hint: str = None) -> list:
    """產生測試案例（使用 Python 迴圈過濾後的精準目錄）"""
    # 1. 在 Python 端做關鍵字過濾，只取出相關目錄（極大節省 Token）
    combined_text = f"{summary} {description} {outline} {path_hint or ''}"
    filtered_tree = filter_relevant_paths(env_type, combined_text)

    # 2. 超極簡 Prompt
    system_prompt = f"""你是一位資深 QA。請將需求轉換為 TestRail 測試案例 JSON Array。

規範：
1. path: 必須 100% 精確匹配此清單中的其中一條：
{filtered_tree}

2. title: [模組]-情境 或 [動作]-目的
3. steps:
   - content 格式：
     1. 路徑：[選取的 path]
     2. [動作/步驟]
     • [具體測試情境]
   - expected: 預期結果，若有錯誤提示用 Tips Red Error Message :

回傳格式（標準 JSON）：
[
  {{
    "title": "提现信息 - 请输入金额",
    "path": "前台 > 首页 > 我的钱包 > 钱包总览 > 提现",
    "preconditions": ["1. 帳號已登入且具備權限。"],
    "steps": [
      {{
        "content": "1. 路徑：前台 > 首页 > 我的钱包 > 钱包总览 > 提现\\n2. 输入金额\\n   • 输入超出范围数字",
        "expected": "Tips Red Error Message :\\n• CN : 提现金额必须介于 n - m 之间。"
      }}
    ]
  }}
]"""

    user_input = f"Jira 摘要：{summary}\nJira 描述：{description}\n測試大綱：\n{outline}"
    if path_hint:
        user_input += f"\n指定優先路徑：{path_hint}"

    raw_text = call_gemini_with_retry([system_prompt, user_input])

    cleaned_text = re.sub(r"^```json\s*", "", raw_text, flags=re.MULTILINE)
    cleaned_text = re.sub(r"^```\s*", "", cleaned_text, flags=re.MULTILINE).strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        raise CaseGenError("AI 回傳格式非有效 JSON，請再試一次。")
