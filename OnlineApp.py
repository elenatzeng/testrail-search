# ... 前面代碼保持不變 (側邊欄、搜尋邏輯) ...

            results.sort(key=lambda x: x[0], reverse=True) 

            for _, item, u in results:
                # ... 📁 Section路徑、c1 c2 標題與按鈕保持不變 ...
                
                with st.expander("查閱測試步驟", expanded=False):
                    steps = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    
                    # 🔥 (10) 強制斷行與格式處理器
                    def final_format(text):
                        if not text: return ""
                        # 移除圖片代碼
                        text = re.sub(img_pattern, '', text).strip()
                        if not text: return ""
                        # 1. 處理已經存在的換行符號，轉為 HTML 斷行
                        text = text.replace('\n', '<br>')
                        # 2. 針對「用户名驗證...」內容進行正則補強 (如果需要加點點)
                        # text = re.sub(r'(?<!<br>)(用户名)', r'<br>• \1', text) 
                        return text

                    if isinstance(steps, list) and len(steps) > 0:
                        v_idx = 1
                        has_any_visible = False
                        for s in steps:
                            c_html = final_format(s.get('content', ''))
                            e_html = final_format(s.get('expected', ''))
                            if not c_html and not e_html: continue
                            
                            has_any_visible = True
                            
                            # 🔥🔥🔥 核心修正：將綠線、標題、黑盒子全部組合為 HTML 字串一次注入
                            full_step_html = f"""
                            <div class="green-line-wrapper">
                                <div class="step-label">Step {v_idx}:</div>
                                <div class="black-box">{c_html if c_html else "(無操作內容)"}</div>
                                <div class="step-label">Expected:</div>
                                <div class="black-box">{e_html if e_html else "(無預期結果)"}</div>
                            </div>
                            """
                            st.markdown(full_step_html, unsafe_allow_html=True)
                            v_idx += 1
                        
                        if not has_any_visible:
                            st.markdown('<div class="no-content-hint">💡 (此案例無文字步驟內容)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="no-content-hint">💡 (此案例目前沒有填寫測試步驟內容)</div>', unsafe_allow_html=True)
                st.markdown("---")

    st.markdown('<a href="#top-anchor" class="scroll-to-top">🚀</a>', unsafe_allow_html=True)
