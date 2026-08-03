import json
import os
import re
import time

import google.generativeai as genai

# --- 將所有目錄精細拆分為列表，方便程式做迴圈尋找 ---

SYSTEM_PATHS = {
    "Web": [
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
        raise CaseGenError(
            "找不到 GEMINI_API_KEY，請在 .streamlit/secrets.toml 或環境變數中設定。"
        )
    genai.configure(api_key=key)


def filter_relevant_paths(env_type: str, text_content: str) -> str:
    all_paths = SYSTEM_PATHS.get(env_type, [])
    if not all_paths:
        all_paths = [p for paths in SYSTEM_PATHS.values() for p in paths]

    matched_paths = []
    for path in all_paths:
        segments = [seg.strip() for seg in path.split(">")]
        for seg in segments[1:]:
            if len(seg) >= 2 and seg.lower() in text_content.lower():
                matched_paths.append(path)
                break

    if not matched_paths:
        matched_paths = all_paths

    return "\n".join([f"- {p}" for p in matched_paths])


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
                    f"模型「{GEMINI_MODEL_NAME}」已不可用。請更換 GEMINI_MODEL_NAME 常數。\n原始錯誤：{err_msg[:300]}"
                )
            else:
                raise CaseGenError(f"API 呼叫失敗：{err_msg}")


def generate_test_outline(summary: str, description: str) -> str:
    prompt = f"請針對以下 Jira 需求，列出測試大綱條目（每行一條重點，不要贅詞）：\n摘要：{summary}\n描述：{description}"
    return call_gemini_with_retry(prompt)


def generate_test_cases(summary: str, description: str, outline: str, env_type: str = "GoGaming", path_hint: str = None) -> list:
    combined_text = f"{summary} {description} {outline} {path_hint or ''}"
    filtered_tree = filter_relevant_paths(env_type, combined_text)

    # 嚴格要求排版與換行規範
    system_prompt = f"""你是一位資深 QA。請將需求轉換為 TestRail 測試案例 JSON Array。

規範：
1. path: 必須 100% 精確匹配此清單中的其中一條：
{filtered_tree}

2. title: [模組]-情境 或 [動作]-目的
3. steps:
   - content 格式（【極度重要】每一項子項目 • 必須強制獨立換行，絕對不可與主要步驟擠在同一行）：
     1. 路徑：[選取的 path]
     2. [動作/步驟]
        • [子項目1]
        • [子項目2]
   - expected: 預期結果，若有細項或錯誤提示，同樣每一點（如 1., 2. 或 •）都必須強制換行。

回傳格式範例（嚴格遵守 \\n 換行）：
[
  {{
    "title": "创建优惠券 - 选择BW现金券校验",
    "path": "GoGaming > 营销推广 > 优惠券管理",
    "preconditions": ["1. 账号已登录且具备优惠券管理与审核权限。"],
    "steps": [
      {{
        "content": "1. 路徑：GoGaming > 营销推广 > 优惠券管理\\n2. 点击“创建优惠券”，选择类型“BW现金券”\\n   • 校验必填栏位与动态选项（币种、金额、提款倍数）\\n   • 校验游戏排除/指定",
        "expected": "1. 显示必填校验提示\\n2. 动态选项正确显示"
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
        cases = json.loads(cleaned_text)
        
        # 【後處理防護機制】：透過 Python 程式強制修復未換行的子項目
        for case in cases:
            for step in case.get("steps", []):
                if "content" in step and step["content"]:
                    # 如果文字中包含子項目點號「•」，但前面不是換行字元 \n，強制插入 \n
                    step["content"] = re.sub(r"([^\n])\s*•\s*", r"\1\n   • ", step["content"])
                if "expected" in step and step["expected"]:
                    step["expected"] = re.sub(r"([^\n])\s*•\s*", r"\1\n• ", step["expected"])
                    
        return cases
    except json.JSONDecodeError:
        raise CaseGenError("AI 回傳格式非有效 JSON，請再試一次。")
