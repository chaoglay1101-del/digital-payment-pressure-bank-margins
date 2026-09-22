import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

print("1. 正在載入原始資料與 Excel 銀行名單...")
df_wrds = pd.read_csv('ASEAN5_Banks_Panel_Data.csv', low_memory=False)
df_excel = pd.read_excel('ASEAN5_listed_commercial_banks.xlsx')

# 自動偵測 Excel 中的銀行名稱欄位
bank_name_col = None
for col in df_excel.columns:
    if 'name' in str(col).lower() or 'bank' in str(col).lower():
        bank_name_col = col
        break
if bank_name_col is None: bank_name_col = df_excel.columns[1]

# ---------------------------------------------------------
# 🛡️ 步驟一：嚴格鎖定東南亞五國
# ---------------------------------------------------------
asean5_codes = ['SGP', 'MYS', 'THA', 'IDN', 'PHL']
df_wrds = df_wrds[df_wrds['fic'].isin(asean5_codes) | df_wrds['loc'].isin(asean5_codes)].copy()

# ---------------------------------------------------------
# 🎯 步驟二：智能名稱比對
# ---------------------------------------------------------
print("2. 正在啟動智能名稱比對演算法...")
def simplify_name(name):
    if pd.isna(name): return ""
    name = str(name).upper()
    name = re.sub(r'\(.*?\)', '', name)
    for word in [' LTD', ' BHD', ' BERHAD', ' CORP', ' CORPORATION', ' INC', ' PLC', ' PT', ' TBK', ',', '.', '-']:
        name = name.replace(word, ' ')
    return " ".join(name.split())

df_wrds['simple_name'] = df_wrds['conm'].apply(simplify_name)
df_excel['simple_name'] = df_excel[bank_name_col].apply(simplify_name)

wrds_unique_names = df_wrds['simple_name'].unique()
matched_w_names = set()
for ex_name in df_excel['simple_name']:
    words = ex_name.split()
    if not words: continue
    if words[0] == 'BANK' and len(words) >= 3: search_key = f"{words[0]} {words[1]} {words[2]}"
    elif len(words) >= 2: search_key = f"{words[0]} {words[1]}"
    else: search_key = words[0]
    for w_name in wrds_unique_names:
        if search_key in str(w_name): matched_w_names.add(w_name)

df_filtered = df_wrds[df_wrds['simple_name'].isin(matched_w_names)].copy()

# ---------------------------------------------------------
# 📚 步驟三：提取深度財務變數
# ---------------------------------------------------------
print("3. 正在提取學術研究所需的深度財務變數...")
academic_cols = [
    'gvkey', 'conm', 'loc', 'fic', 'fyear', 'datadate', 'curcd', 'indfmt',
    'revt', 'idit', 'xint', 'initb', 'bcef', 'cfo', 'ib', 'ni', 'pcl',
    'at', 'che', 'ivst', 'custadv', 'liqresn', 'intan', 'ppent',
    'dptb', 'dptc', 'dltt', 'ceq', 'seq', 'lct', 'txp'
]

keep_cols = [c for c in academic_cols if c in df_filtered.columns]
df_final = df_filtered[keep_cols].copy()

financial_cols = [c for c in keep_cols if c not in ['gvkey', 'conm', 'loc', 'fic', 'datadate', 'curcd', 'indfmt']]
for col in financial_cols:
    df_final[col] = pd.to_numeric(df_final[col], errors='coerce')

# ---------------------------------------------------------
# 🛠️ 步驟四：缺失值處理 (放寬標準版)
# ---------------------------------------------------------
print("4. 啟動缺失值診斷與處理機制...")

# 策略 A：手續費與準備金科目，合理補零
fill_zero_cols = ['pcl', 'bcef', 'cfo', 'ivst', 'liqresn', 'initb']
for col in fill_zero_cols:
    if col in df_final.columns:
        df_final[col] = df_final[col].fillna(0)
        
# 策略 B：【修正】只剔除連「總資產(at)」都沒有的幽靈樣本，保留其他缺失值以維持樣本數
before_drop = len(df_final)
if 'at' in df_final.columns:
    df_final = df_final.dropna(subset=['at'])
after_drop = len(df_final)
print(f"-> 僅剔除缺乏「總資產(at)」的無效樣本共 {before_drop - after_drop} 筆。")

# ---------------------------------------------------------
# 📈 步驟五：複合指標計算
# ---------------------------------------------------------
print("5. 正在計算財務比率與模型變數...")
if 'che' in df_final.columns and 'at' in df_final.columns:
    df_final['Liquidity_Ratio_LC1'] = df_final['che'] / df_final['at']
if 'custadv' in df_final.columns and 'dptb' in df_final.columns:
    df_final['L_D_Ratio'] = df_final['custadv'] / df_final['dptb']
if 'ceq' in df_final.columns and 'at' in df_final.columns:
    df_final['Capital_Adequacy_Proxy'] = df_final['ceq'] / df_final['at']
if 'initb' in df_final.columns and 'at' in df_final.columns:
    df_final['Net_Fee_Margin'] = df_final['initb'] / df_final['at']

# ---------------------------------------------------------
# 💾 步驟六：輸出最終結果
# ---------------------------------------------------------
sort_cols = [c for c in ['fic', 'loc', 'conm', 'fyear'] if c in df_final.columns]
df_final = df_final.sort_values(by=sort_cols)

output_filename = 'Academic_Bank_Panel_Data_Cleaned.csv'
df_final.to_csv(output_filename, index=False)

print("-" * 50)
print(f"✅ 大功告成！")
print(f"-> 成功保留有效面板數據：{after_drop} 筆！")
print(f"-> 檔案已成功儲存為：{output_filename}")