# 數位支付壓力與銀行淨手續費利潤率

**大學會計與金融研究作品集｜東協三國銀行面板資料**

[English version](README.md)

## 研究問題

本研究探討數位支付活動是否與銀行淨手續費利潤率具有關聯。研究原先規劃涵蓋 ASEAN-5，但因 IMF Financial Access Survey 的選定指標在菲律賓與新加坡的資料涵蓋不一致，最終分析樣本為印尼、馬來西亞與泰國。

## 研究動機

數位支付可能為銀行帶來新的交易機會，也可能加劇傳統支付服務的價格競爭，壓縮手續費收入。本研究以銀行層級財務資料結合國家年度數位支付指標，檢驗這兩種可能方向。

## 主要成果

- 建立涵蓋 **39 家銀行、344 筆 bank-year observations** 的面板資料。
- 研究期間為 **2014-2022 年**，涵蓋印尼、馬來西亞與泰國。
- 使用 Python、pandas 與 `linearmodels` 進行資料清理、變數建構與面板迴歸。
- 使用銀行與年度固定效果、銀行群聚標準誤，以及 1%/99% winsorisation。
- 加入 log transformation、銀行規模交互作用、非線性模型與國家子樣本分析。

## 主要發現

- 線性基準模型對直接關聯的統計證據有限。
- Log specification 顯示數位支付壓力與銀行淨手續費利潤率之間存在負向且具統計顯著性的 pooled association。
- 國家子樣本結果並不一致，分解分析也顯示 pooled result 可能主要反映國家間的結構差異，而不是每個國家內都存在相同的作用機制。

| 模型 | 數位支付係數 | 觀測值 | 解讀 |
| --- | ---: | ---: | --- |
| 線性主模型 | -0.000292* | 344 | 負向關聯；邊際顯著 |
| 完整控制變數模型 | -0.000208 | 344 | 負向關聯；未達統計顯著 |
| Log baseline model | -0.010171** | 344 | 負向且具統計顯著性的 pooled association |
| 非線性模型線性項 | -0.010829** | 344 | 負向；平方項未達顯著 |

`* p < 0.10`，`** p < 0.05`。

## 資料與方法

數位支付壓力變數來自 IMF Financial Access Survey indicator `IMF_FAS_FCMIBT`，測量單位為 `PT_GDP`，代表手機與網路銀行交易金額占 GDP 的比例。銀行資料來自受限制的 WRDS-derived bank panel，因此完整論文迴歸不能由公開 repository 直接重跑。

公開 repository 提供一個不含受限資料的 synthetic fixed-effects demonstration，讓讀者可以檢查 Python 與 `linearmodels` 的基本工作流程：

```powershell
uv sync --group dev
uv run python examples/run_example.py
uv run pytest
```

## 公開研究報告

完整論文、課程提交版本與受限制資料不公開於 GitHub；但研究問題、方法、結果與限制已整理為可直接閱讀的英文版 [公開研究報告](docs/public-research-report.md)。該報告保留研究設計與結果解讀，並清楚說明哪些資料不可重分發、哪些分析只能透過合成資料示範檢視。

## Repository 導覽

- [完整公開研究報告（英文）](docs/public-research-report.md)
- [研究流程與資料決策](docs/research-process.md)
- [主要迴歸程式](src/analysis/run_main_regressions.py)
- [國家子樣本穩健性分析](src/analysis/run_country_subsamples.py)
- [公開 synthetic example](examples/run_example.py)
- [MIT License](LICENSE)

## 研究限制

以上結果是 conditional associations，不是因果估計。主要限制包括：數位支付變數只在國家年度層級變動、最終樣本只有三個國家、WRDS-derived data 不能公開，以及可能存在遺漏變數。研究結果應解讀為 ASEAN-3 銀行市場的實證關聯，而不是 ASEAN-5 或所有銀行市場的普遍因果結論。
