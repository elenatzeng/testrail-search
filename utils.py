import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html).strip()
    
    # 🚀 1. 處理 TestRail 分離步驟 (Separated Steps)
    # 如果內容看起來像 Python 清單格式
    if text.startswith('[') and ('content' in text or 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                # 再次清理清單內每個欄位的標籤
                for item in parsed_data:
                    for key in ['content', 'expected']:
                        val = item.get(key, '')
                        # 清除 <img...>, <br...>, &nbsp; 並移除所有 HTML 標籤
                        val = re.sub(r'<img[^>]*>', '', val)
                        val = val.replace('<br />', '\n').replace('<br>', '\n')
                        val = val.replace('&nbsp;', ' ')
                        val = re.sub(r'<.*?>', '', val)
                        
                        # 💡 終極換行修復：遇到關鍵動作詞，強制分行
                        split_keys = ["路徑", "選擇", "URL", "點擊", "点击", "登入", "查看", "成功"]
                        for word in split_keys:
                            # 如果這個詞前面沒有換行符號，就幫它加一個
                            val = re.sub(f'(?<!\\n)({word})', r'\n\1', val)
                        
                        item[key] = val.strip()
                return parsed_data 
        except:
            pass

    # 🚀 2. 處理普通純文字 (清理 <br>, <img>, 移除所有標籤)
    text = re.sub(r'<img[^>]*>', '', text)
    text = text.replace('<br />', '\n').replace('<br>', '\n')
    text = text.replace('&nbsp;', ' ')
    # 移除剩餘 HTML 標籤
    text = re.sub(r'<.*?>', '', text)
    
    # 💡 同樣的換行修復邏輯
    split_keys = ["路徑", "選擇", "URL", "點擊", "点击", "登入", "查看", "成功"]
    for word in split_keys:
        text = re.sub(f'(?<!\\n)({word})', r'\n\1', text)
        
    return text.strip()

# ... (multi_lang_search 與 fetch_data_from_tr 函數維持不變)
