# 聯發科(2454) 每日日報
產生時間：2026-11-27 10:41 (台北)　資料日：2026-11-26　收盤：3705.0　模式：即時模式(手動)

## 次一交易日預測
- **上漲 38% ／ 盤整 11% ／ 下跌 51%** → 略偏空（上漲−下跌 -13 個百分點），信心：中
- 規則化因子加權均分(-10~+10；我訂的簡易規則，非模型輸出，與預測機率不同)：-0.3
- 模型輸入：37 個特徵(含法人籌碼)

## 樣本外回測(滾動式，不偷看未來)
- 回測天數：606；訓練視窗 500 日，每 20 日往前滾動
- 三分類命中率：**48.0%**(永遠猜最常見類別基準線：40.6%)
- 漲跌方向命中率(排除盤整日，共 495 天)：**61.0%**(永遠猜漲基準線：49.7%)
- 是否達成 90% 目標：**否**　(長期穩定的次日預測，超過 60% 就已非常罕見；若回測出現 90% 以上，應先懷疑資料洩漏或過擬合)

## 實盤追蹤(本腳本每日預測 vs 實際)
- 已驗證 23 天；三分類命中 47.8%；方向命中 50.0%(n=22)

- 已驗證 22 天；三分類命中 11/22（50%，純猜約 33%）。有明確方向（上漲與下跌機率差≥8 個百分點）且實際非盤整的判斷 19 次，命中 10 次（53%，95% 信賴區間 32%–73%；純猜約 50%）。樣本少時區間很寬，無法據此判斷模型好壞；紀錄也混有不同版本的模型。

## 聯發科新聞：今日 11/27（8 則報導 → 7 個事件）
- 11/27 09:27 台股開盤百點震盪！「PCB大廠」連拉2漲停、健策點火亮燈 聯發科、創意、世芯ASIC全中刀（Yahoo股市） https://news.google.com/rss/articles/CBMi-gJBVV95cUxQdHhmRXJpZnpXUW9lR2xCaDAwejlaZzlpSEdMN0twdkstZFJBak1jdVBTWkxzUE1jQkM4SjJocF9hOGU1dm5zM2lvYWk1RXJZc1NNMGJTWE9GMzBGdFBlcDNyVHdsM29nNHJRY3RJVFBpQl9Fa1NLZHVRc1R2UnR0SzNMM2FOUDBvcnFNdjRJZldJUVBONk12X3lvRU0wZ1MxWURucGJHaXgwcS1namw4RWJaR2pVTndpWDlrYVlFeWt6MEIxVmlwdDNtck9lcUs2SmhxTG9hdDEzQjlwaHY2WVdOMjA5YUNnbnJnTWpqbTU1ZlRONl9icmlkZXV4ZVFUeUxGdmM0bjJUSVlvQ2hmZW45UVpINGQ2a0JXYzhiMzhGVzV3LWh2UlFmXzdoSlJXcWVRMk5vaVBPRng5RnpMRnl1b0psTDJSZ0NXM1loVVFrNGlGWG9yb1FPbGdxenJBTmFmeUF6cUx3LTZzWnY5MzVhOEZoZTJnZ3c?oc=5
- 11/27 09:23 MediaTek confirms 2027 flagship mobile SoC launch, dismisses cancellation rumors（digitimes） https://news.google.com/rss/articles/CBMijwFBVV95cUxPNURIQmUwYkxXcVZWZnc5STJXa2hSTzVVRW9ZYkVxQ21FampjcEFONnBnS1lrc3hUZkU3eWY0VlNwdWtUYlEtdnE4eVc5QUhjY21OaEViMEpndWFNemZxMW9vYkRTMDRwbXdhUFVfQkxtalNDSGZ0dzZnT21tUHQwMUs2TGxCcnh0d2lHWGdmRQ?oc=5
- 11/27 09:23 2454 聯發科 - 低接- 股市爆料同學會（CMoney） https://news.google.com/rss/articles/CBMiWEFVX3lxTFBRSHlNMkd1S3pNTko5N1lReVNvMjQ5cVRXdjhWbC1NZkxJbUNkSklOMHV3TmZmRjNFaFpJX1NPeFpMTFozSng2SWIyeFFVVEJOR3VadlN2SWY?oc=5
- 11/27 09:18 台股多空激戰3萬9！聯發科、台達電翻黑 台積電能扛住？ | 市場焦點 | 證券（×2：UDN、經濟日報） https://news.google.com/rss/articles/CBMid0FVX3lxTE1lY2JXX2xJSnhIUFh5WnB6UkdrenFYd2VsTE9fbW9aOFl5TW9obHZGOTJXb19LRmJhaDNuOUh4dFZPNVBPWk11akZJRXl6UDZPZXA2U3B6cFR2X2s5YTRMbERHdjdndHBnRlM0M3A3NE5LcFFjZE1V?oc=5
- 11/27 08:01 《半導體》拉貨轉弱 聯發科手機營收承壓（富聯網） https://news.google.com/rss/articles/CBMiiAFBVV95cUxQSnpwM0VOMzhYTEJ6a0pHQXZSQ2pyU2VoSUdKc1ZBbDFNZGhKeW9nRlFERERSREF2eFotV0d0ZnBac0hVMjZKZXd2V1lDUzhsMXVYSWY4ZF9LRXNlY3ZyR0hoaVRUVTNsMEFwSUZ2cGhkeXNYUmZlcDJVMEZWY0xNZkFHY0FjYWhG?oc=5
- 11/27 05:06 MediaTek Inc. (2454.TW) Stock Price, News, Quote & History（Yahoo! Finance Canada） https://news.google.com/rss/articles/CBMiVkFVX3lxTE5EVVZuZ3pWN1Z3VVFGYWk3b1FHdHBxZ0oxYUtkUTlKQXNERktVNnI5bVdYb3gwZ1plVi1hYVZFQXFkWF9peURQR1V0eXZsY29KczZQbW1B?oc=5
- 11/27 03:15 台股大跌1683點摜破45000點 聯發科跌停剩49千金（經濟日報） https://news.google.com/rss/articles/CBMie0FVX3lxTE92N01EcEpDRm42WXpFamNCYjRTZ1RlcDlWVFZvUF94RTJjZV9vbS01TjYweUF6ZmJ6dEV0VnJNYXV0QmhMNTdfQWpTU0VhTndpT2VMQ3BJRmhHQm1ONTdvLUMwal9KR0hONHlQYk9mdzNDZGQySHkyTmc4RdIBX0FVX3lxTE1kbExDNm5TLXJ6TFZGUHdKeUVrYTAzcXR2STlBckZPdVFFbWJKUkFUZldRVExmbld2ZW5WSGxZRjdNVVNMX1FNRmp6bUpPYVJQRG1DQ3lXdVRRdkd0c1VV?oc=5
- 註：僅即時版（手動更新）顯示，不進預測模型；來源 Google News，只列標題含聯發科／發哥／2454／MediaTek 者，可能漏列，請自行判讀。

## 自上次執行以來的變化（即時版，2026-11-26 16:38）
- 預測機率：上漲 31%→38%（+7 個百分點）／盤整 12%→11%／下跌 58%→51%
- 規則分數變動較大：美元兌新台幣 -2→-10、那斯達克期貨(夜盤參考) +1→+7、融資融券餘額變化 +2→-2、外資近5日買賣超(聯發科) -7→-5、外資持股比例變化 -8→-6、烏俄戰爭進度 +3→+1
- 即時行情漲跌：Google +0.71%→+0.71%、博通 +1.17%→+1.17%、高通 +0.81%→+0.81%
- 新出現的新聞標題：
  - [烏俄] 劉燕婷觀點：俄烏戰爭歐洲入場─抗衡美國與俄羅斯，意外的Game Changer？ - Storm.mg（11/26）
  - [烏俄] 要聞分析 - 感恩節之際特朗普敦促普京停戰 歐盟啟動第22輪對俄制裁 - RFI（11/26）
  - [烏俄] 川普稱已敦促普丁停止侵略歐洲 盼俄烏迅速達成協議 - 信吉衛視+（11/26）
  - [烏俄] 札波羅熱核電廠外部電力中斷 IAEA協調俄烏局部停火搶修 - 民視新聞網（11/27）
  - [烏俄] 川普會晤北約秘書長 籲俄勿擴大烏克蘭戰爭 - Rti 中央廣播電臺（11/26）
  - [烏俄] 川普稱已敦促普亭停止侵略歐洲 盼俄烏迅速達成協議 - 世界新聞網（11/26）
  - [烏俄] 烏克蘭「強制徵兵」亂象曝！警上街暴力強押 他遭踹頭、噴辣椒水 - TVBS新聞（11/26）
  - [烏俄] 俄烏能源攻防持續 拉脫維亞總統估明年戰局或現轉折 - Taiwan News（11/25）
  - [烏俄] 波蘭籲在烏攔截飛彈呂特：準備「直接軍事對抗」 北約「這2國」秘通俄| 國際 - Newtalk新聞（11/26）
  - [烏俄] 王立本觀點：從黑海到班加西─無人機如何把俄烏戰爭推向全球海上消耗戰 | 王立本 | 評論 - Storm.mg（11/26）
- 註：新聞不進預測模型，新聞本身不會改變上漲／下跌機率；機率的變化只來自股價、匯率、盤後價等市場資料。新聞請自行判讀。

## 方案比對：即時版 vs 標準版
- 已累積可比對交易日：**7/10**（共 12 次即時執行，同一天多次取機率平均；待驗證 2 筆）
- 滿 10 個交易日後顯示初步比對。任何時間手動執行都會被記錄。

## 即時行情(即時版預測已套用)
- Google(GOOGL)：正規盤收 272.95 → 最新 274.89（+0.71%，盤後，11/26 08:59 台北）
- 博通(AVGO)：正規盤收 300.49 → 最新 304.00（+1.17%，盤後，11/26 08:59 台北）
- 高通(QCOM)：正規盤收 168.61 → 最新 169.97（+0.81%，盤後，11/26 08:59 台北）
- 已套用：Google +0.00%→+0.71%、博通 +0.00%→+1.17%、高通 +0.00%→+0.81%
- 標準版預測(不含即時資料)：上漲 38% ／ 盤整 11% ／ 下跌 50%

## 參考價位(情境，以目前價位 3705.0 計)
- 上漲情境：3827.9（+3.32%）／盤整：3706.8（+0.05%）／下跌：3613.1（-2.48%）
- 機率加權預期價：**3705.5（+0.01%）**　※訓練期各類別平均報酬的統計值，非保證

## 模型實際看法(與下表顯示分數無關)
- 推高「上漲」最多：投信5日買賣超(+0.11)、60日均線乖離(+0.09)、布林位置(+0.08)、VIX變化(+0.05)、高通(+0.05)
- 壓低「上漲」最多：VIX水準(-0.22)、20日漲跌(-0.13)、瑞昱(-0.12)、布蘭特油價(-0.05)、KD-K值(-0.05)

## 32 項因子
| # | 類別 | 因子 | 最新值 | 規則分數(-10~+10) | 模型貢獻 | 來源 |
|---|---|---|---|---|---|---|
| 1 | 籌碼 | 外資近5日買賣超(聯發科) | -7,030 張 | -5 | -0.03 | FinMind/模型 |
| 2 | 籌碼 | 投信近5日買賣超(聯發科) | 1,856 張 | +1 | +0.11 | FinMind/模型 |
| 3 | 籌碼 | 自營商近5日買賣超(聯發科) | 354 張 | +0 | +0.00 | FinMind/模型 |
| 4 | 籌碼 | 三大法人合計(依張數加總) | -4,820 張 | -4 | — | FinMind/模型 |
| 5 | 籌碼 | 外資持股比例變化 | 51.44%（5日 -0.48 個百分點） | -6 | -0.04 | FinMind/模型 |
| 6 | 籌碼 | 融資融券餘額變化 | 融資 11,560 張（5日 +3.31%）／融券 32 張（5日 -23.81%） | -2 | -0.03 | FinMind/模型 |
| 7 | 籌碼 | 成交量/20日均量 | 1.07x | +1 | +0.02 | 模型 |
| 8 | 技術 | 相對5/20/60日均線 | 1/3 條之上 | -1 | +0.08 | 模型 |
| 9 | 技術 | RSI(14) | 46.2 | -1 | +0.02 | 模型 |
| 10 | 技術 | KD與MACD | K=46, MACD柱=+0.50% | +0 | -0.03 | 模型 |
| 11 | 技術 | 布林通道位置 | -0.15 | -1 | +0.08 | 模型 |
| 12 | 技術 | 20日支撐/壓力位置 | 53% (0=低點,100=高點) | +0 | +0.02 | 模型 |
| 13 | 國際 | 美股四大指數(前一美股日) | +0.00% / +0.00% / +0.00% / +0.00% | +0 | -0.01 | 模型 |
| 14 | 國際 | VIX恐慌指數 | 26.8 (-5.27%) | +3 | -0.17 | 模型 |
| 15 | 國際 | 那斯達克期貨(夜盤參考) | +2.04% | +7 | — | 僅參考 |
| 16 | 國際 | 美元指數/美債10年 | DXY +0.03% / 10Y +0.000 | +0 | -0.01 | 模型 |
| 17 | 國際 | 美元兌新台幣 | +0.81% | -10 | +0.04 | 模型 |
| 18 | 產業 | 費半與台積電 | SOX +0.00% / 台積電 -0.23% | +0 | -0.05 | 模型 |
| 19 | 產業 | 高通/博通/聯詠/瑞昱 | +0.00% / +0.00% / +4.33% / +4.43% | +4 | -0.06 | 模型 |
| 20 | 產業 | 手機/AI邊緣晶片需求 | 熱度 8 則｜三大利空影響…手機市況依舊低迷 - 經濟日報（11/26） ｜ 【即時新聞】鈺創董座盧超群看好AI商機！受惠記憶體供需吃緊訂單直達明年 - CMoney投資網誌（11/26） | +0 | — | 新聞關鍵字(粗略) |
| 21 | 產業 | 月營收與法說指引 | 熱度 10 則｜聯發科（2454）做什麼？Q3財報優於預期，股價為什麼又跌停？，AI ASIC成長動能完整解析｜豐雲學堂2026 年 11 月 - 永豐金證券（11/25） ｜ 大賣空〝貝瑞〞都反手多了!! 買價值、買成長、買被錯殺 / 陳學進的貼文 / 鉅亨號 / Anue鉅亨 - 鉅亨號（11/26） | +1 | — | 新聞關鍵字(粗略) |
| 22 | 產業 | Google(GOOGL)正規盤收盤漲跌 | +0.00% | +0 | -0.04 | 模型 |
| 23 | 產業 | Google(GOOGL)盤後最新價 | 收盤 272.95 → 最新 274.89（+0.71%，11/26 08:59 台北）（即時版預測已套用） | — | — | 即時(yfinance) |
| 24 | 產業 | Google TPU×聯發科新聞(中文) | 熱度 45 則｜聯發科有望受惠！Google砍博通TPU訂單百萬顆、2027年出貨量下修20% - 鉅亨網（11/22） ｜ 再奪Google TPU大單！聯發科獲大摩高喊6188元目標價 前三季EPS衝47元 - Yahoo股市（11/22） | -1 | — | 新聞關鍵字(粗略) |
| 25 | 產業 | Google TPU 國際新聞(英文) | 熱度 11 則｜Google's TPU challenges Nvidia, opening a path for MediaTek to dominate ASIC supply - digitimes（11/20） ｜ Broadcom Plunges 11% as Google Reportedly Shifts TPU Orders to MediaTek, Overshadowing Goldman's $460 Target; Marvell Sinks 10% - 24/7 Wall St.（11/20） | +2 | — | 新聞關鍵字(粗略) |
| 26 | 產業 | Alphabet AI晶片/資本支出動態 | 熱度 18 則｜Key facts: Alphabet raises AI capex; Search slows; FCF turns negative - TradingView（11/21） ｜ Google shifts some '27 high-end AI chip orders from Broadcom to MediaTek, Ming-Chi Kuo says - Seeking Alpha（11/20） | +1 | — | 新聞關鍵字(粗略) |
| 27 | 總經 | 國際油價(WTI/布蘭特) | +0.00% / -2.57% | +4 | -0.05 | 模型 |
| 28 | 總經 | 烏俄戰爭進度 | 熱度 22 則｜劉燕婷觀點：俄烏戰爭歐洲入場─抗衡美國與俄羅斯，意外的Game Changer？ - Storm.mg（11/26） ｜ 要聞分析 - 感恩節之際特朗普敦促普京停戰 歐盟啟動第22輪對俄制裁 - RFI（11/26） | +1 | — | 新聞關鍵字(粗略) |
| 29 | 總經 | 美伊(中東)局勢 | 熱度 16 則｜科威特遭無人機攻擊2義大利人喪生伊朗否認涉案/ 中東戰火連綿/ 全球 - UDN（11/26） ｜ 【中東戰局】美國討論清除伊朗“強硬派人物” - 鉅亨號（11/26） | -2 | — | 新聞關鍵字(粗略) |
| 30 | 總經 | 美中科技管制與關稅 | 熱度 62 則｜美國收緊AI晶片管制駐泰業者：部分投資案暫停、對前景仍樂觀/ 產經 - 中央社 CNA（11/26） ｜ 惠譽：美國晶片出口新管制將拖慢亞太區資料中心投資/ 全球財經/ 全球 - UDN（11/26） | -5 | — | 新聞關鍵字(粗略) |
| 31 | 總經 | 聯準會利率預期 | 熱度 33 則｜市場預計聯準會持續升息之際 債券交易員卡位2028年激進降息 - 鉅亨網（11/25） ｜ 美國經濟成長 4.3%、通膨還降不下來，聯準會還會降息嗎？-下午先生 - CMoney投資網誌（11/26） | -1 | — | 新聞關鍵字(粗略) |
| 32 | 總經 | 外資券商目標價/評等 | 熱度 16 則｜AI需求旺！外資續喊買封測雙雄日月光目標價上到9字頭- 日報 - 工商時報（11/26） ｜ AI ASIC 動能強勁，花旗維持聯發科買進評等目標價 6,800 元 - TechNews 科技新報（11/26） | +2 | — | 新聞關鍵字(粗略) |
| | **模型合計** | 其他特徵(近期漲跌、加權指數等) | | | -0.10 | |
| | | 基準傾向(截距：訓練期上漲日 vs 下跌日) | | | -0.02 | |
| | | **合計 ln(上漲/下跌)** | | | **-0.28** | |

> 註：「新聞關鍵字」僅對標題做正負詞計數，非真正語意判斷，無歷史資料可回測，未納入模型；融資增加視為偏空僅為顯示用的經驗規則。分數為顯示用的規則化評價，模型權重由歷史資料估計。
> 時間說明：每日台北約 06:00 執行：美股為前一美股日完整收盤；美股盤後交易要到台北約 09:00 才結束，Google 盤後價為執行當下的最新價(yfinance 盤後資料可能延遲或缺漏)。
> 本報告僅供參考，不構成投資建議。