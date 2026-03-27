def multi_lang_search(text, dictionary):
    if not text: return []
    t_lower = text.lower().strip()
    res = {t_lower} # 👈 這裡最重要！初始值必須包含原文自己
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)
