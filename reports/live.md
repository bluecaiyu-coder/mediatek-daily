# 聯發科(2454) 每日日報
產生時間：2026-11-25 09:16 (台北)　資料日：2026-11-24　收盤：4050.0　模式：即時模式(手動)

## 次一交易日預測
- **上漲 7% ／ 盤整 23% ／ 下跌 71%** → 明顯偏空（上漲−下跌 -64 個百分點），信心：高
- 規則化因子加權均分(-10~+10；我訂的簡易規則，非模型輸出，與預測機率不同)：-0.4
- 模型輸入：37 個特徵(含法人籌碼)

## 樣本外回測(滾動式，不偷看未來)
- 回測天數：606；訓練視窗 500 日，每 20 日往前滾動
- 三分類命中率：**49.3%**(永遠猜最常見類別基準線：40.3%)
- 漲跌方向命中率(排除盤整日，共 495 天)：**62.6%**(永遠猜漲基準線：49.7%)
- 是否達成 90% 目標：**否**　(長期穩定的次日預測，超過 60% 就已非常罕見；若回測出現 90% 以上，應先懷疑資料洩漏或過擬合)

## 實盤追蹤(本腳本每日預測 vs 實際)
- 已驗證 21 天；三分類命中 47.6%；方向命中 50.0%(n=20)

- 已驗證 21 天；三分類命中 10/21（48%，純猜約 33%）。有明確方向（上漲與下跌機率差≥8 個百分點）且實際非盤整的判斷 18 次，命中 9 次（50%，95% 信賴區間 29%–71%；純猜約 50%）。樣本少時區間很寬，無法據此判斷模型好壞；紀錄也混有不同版本的模型。

## 聯發科新聞：今日 11/25（7 則報導 → 7 個事件）
- 11/25 09:10 鴻海崩7%、聯發科挫6%！台積電大跌140元至2090元 台股開低暴跌2061點跌破39000點大關（FTNN 新聞網） https://news.google.com/rss/articles/CBMiS0FVX3lxTFA2OWttekVnMXFzQlJzQWNKTF9TOHBROVY5N2hhSmlpMV9rTU52ZmlkZ0ZtcnkxMUxBTXlpaGozNmF5UkJmZDlNWVlSbw?oc=5
- 11/25 08:58 2454 聯發科 - 昨天一堆被趁機倒貨，唯獨聯發科沒有被倒 - 股市爆料同學會（CMoney） https://news.google.com/rss/articles/CBMiWEFVX3lxTE1RQk9yNVpMbFd1dXJaNGhrelkzS3loM0RJa2hEWE82LWpGSWV1N0F2YlB3dTVzMTBXQzBFX1k0WHdfbllSUjBTODBlaEVCWEhQN3I0MDM0NmM?oc=5
- 11/25 08:48 2454 聯發科 - 陸外資佈空單超過十萬口，小心！ - 股市爆料同學會（CMoney） https://news.google.com/rss/articles/CBMiWEFVX3lxTFBIaVBvQzhJdFhOYlZLOW9OQ2x6WTdhSlVJaWNOcnJtV1FVeDhlUkluUDhoNmE4aXk4RVIyYTFidUxQVk84STdDZzgwNS1ZQlY4UDhuclgzYko?oc=5
- 11/25 05:44 漲停潮後誰還能撿？杜金龍喊年底5萬點不變聯電、南亞、聯發科和「這檔ABF」入列：反彈上看50％ - 上市櫃（旺得富理財網） https://news.google.com/rss/articles/CBMiakFVX3lxTFB5X1R3T0FQYkFSVkhUM25pMUpBX2dELWIxcXlLaU5sUHRqUFRoQ2NqcWxseXpqcE1oZzFnNzNNT0hsQUE5OEZRQ0dIUDlsa2ZTVGVkdG14WU82ektnZ09SbHc0OVoydFk4aXc?oc=5
- 11/25 04:23 GIGABYTE’s GC-WF7LITE Wi-Fi 7 Cards Move To Realtek And MediaTek 160 MHz Modules With A Single Combined Antenna Adapter And No Onboard USB Port（Wccftech） https://news.google.com/rss/articles/CBMi9wFBVV95cUxPNG90VzRLRTNya1dRTml0NUVMTmx4SUVVeTc2NEJjQW5TbGpLN1hTekk3bjRpRmVQbnMwaEowNG5SMEJiMlBCbU51eWZHZ1FoMWI2RmYyRUE3eTRDcld3MlYzanpQUkdiYjFHVUJJZGFwTHVNNHQ1eGg3N2hZT1JMendPcFV5ZFRXLXI0SEtzVHlkZmc1MHpPTXZXN1pTTDFoSXNjNTNnTGNBVm9CNjhOaVhxN1EtV0ZjeFRsSjJULUtvYWg1bVZndVdFOS1XU1RuUmdMZnE2Y2hDY3c0N09NTUdhWkVOZ2FxYWVQVXBIZXA3YjJBc25N0gH8AUFVX3lxTE1ZQkZ0aHYxci1pQkVVaWpyNGp4dnBFUjNISFBTT3lrR2Q2bmx3ZHBNaTN2b205TVJoT0h6T3hIS1kxT0FiWWRVMk9TRHFsdDdnOXhHWUxCLU9PdkM0MUVvQzBtTG11MzUtYWRhbmxSc05NX3Z5S0p6NW9IRTQwdE1tYnh1MmZURGFxSklERHNVWXZJXy00UnV5SjBQbERZR3EtVm1WVUR1QWZ3TzVnQmY5Y0dhTVBYbHlMc2hLbWZ2SUdlQy1SeUljQ3ZEaXJRcGpXLUkzVG9Ld0h5RHpsRGtWcTRVcThQRU9vd25VTmdsV1BPU0RZV1QtclZRZA?oc=5
- 11/25 02:42 討論牆 | 從邊緣AI到雲端AI，聯發科17篇論文入選國際期刊（LINE TODAY） https://news.google.com/rss/articles/CBMiZEFVX3lxTE10M2hhcURaand0eXE0aTZXX2xNLWJpU3psVW5IalVtUll0NnlNams0ejFUNVF1UnF6LVBLU3FqOUZ3dm1BYW5HcTY0dzJtRG5jSFEyWXV2aENpVWJlTng2Y0NMVkY?oc=5
- 11/25 00:28 台積、聯發科 認購旺（經濟日報） https://news.google.com/rss/articles/CBMiWkFVX3lxTE9SNTJ6Q3BUSm1EaVB4a2VCZVpqSXV6cTVGdG5QTGJMX1RhMFR4Vk40M1NqLTI0M05yQi1DdTNhd0tlajU3MmxtWmF2NHhSLUZqRGhWNXRKLWF6d9IBX0FVX3lxTE8xaXBtOGpFSjBLYXozd21HZUtpcHU5SExudFo5TlAteXRUS05ncGk2MGNjcmpOdERJMlpnYWVSSHRnMC1sMXZsX1l0SEhFbTQtR0JhUE1OQkxHX2VqLWtZ?oc=5
- 註：僅即時版（手動更新）顯示，不進預測模型；來源 Google News，只列標題含聯發科／發哥／2454／MediaTek 者，可能漏列，請自行判讀。

## 自上次執行以來的變化（排程版，2026-11-24 14:22）
- 預測機率：上漲 19%→7%（-13 個百分點）／盤整 25%→23%／下跌 56%→71%
- 規則分數變動較大：那斯達克期貨(夜盤參考) +1→-9、費半與台積電 +5→+0、美元指數/美債10年 +0→+4、國際油價(WTI/布蘭特) +3→-1、美股四大指數(前一美股日) +0→-3、融資融券餘額變化 -3→-5
- 新出現的新聞標題：
  - [烏俄] 俄烏戰爭未歇…估超過70萬俄軍陣亡 逾1000士兵輕生 - 世界新聞網（11/24）
  - [烏俄] 俄烏戰爭恐迎轉折點？拉脫維亞總統曝俄國明年恐面臨挫敗 | 民視新聞網 - LINE TODAY（11/24）
  - [烏俄] 梅蘭妮亞迎白宮聖誕樹！許願俄烏聖誕節前停火、盼世界和平 - 中天新聞網（11/24）
  - [美伊] 伊朗高調公開「地下飛彈城」內部 標語嗆美國：混蛋 - UDN（11/24）
  - [美伊] 卡塔爾警告，中東無法承受美國與伊朗之間的再次升級 - FXStreet（11/23）
  - [美伊] 中東緊張升高未擋油價跌勢 全球成長放緩疑慮成焦點 - 商傳媒（11/23）
  - [美伊] 美國｜據報正調查伊朗涉50艘運油輪遭網絡攻擊 - 香港經濟日報HKET（11/24）
  - [美伊] 川普斥談判無意義 傾向明年初對伊朗發動新一輪軍事打擊 - 世界新聞網（11/24）
  - [美伊] 伊朗革命衛隊稱3艘油輪荷莫茲觸雷起火 指美軍空中護航未能阻止 - 蕃新聞（11/24）
  - [美伊] 中東局勢撲朔迷離！談判僵局難破之際特朗普威脅明年恢復對伊動武以色列醞釀單獨襲伊作者智通財經 - Investing.com 香港 - 股市報價& 財經新聞（11/23）
- 註：新聞不進預測模型，新聞本身不會改變上漲／下跌機率；機率的變化只來自股價、匯率、盤後價等市場資料。新聞請自行判讀。

## 方案比對：即時版 vs 標準版
- 已累積可比對交易日：**6/10**（共 11 次即時執行，同一天多次取機率平均；待驗證 1 筆）
- 滿 10 個交易日後顯示初步比對。任何時間手動執行都會被記錄。

## 即時行情(即時版預測已套用)
- Google(GOOGL)：正規盤收 279.03 → 最新 278.88（-0.05%，盤後，11/25 08:59 台北）
- 博通(AVGO)：正規盤收 301.23 → 最新 302.55（+0.44%，盤後，11/25 08:59 台北）
- 高通(QCOM)：正規盤收 164.97 → 最新 163.68（-0.78%，盤後，11/25 08:57 台北）
- 已套用：目前無可套用的即時資料
- 標準版預測(不含即時資料)：上漲 7% ／ 盤整 23% ／ 下跌 71%

## 參考價位(情境，以目前價位 4050.0 計)
- 上漲情境：4184.7（+3.33%）／盤整：4052.0（+0.05%）／下跌：3950.5（-2.46%）
- 機率加權預期價：**3988.8（-1.51%）**　※訓練期各類別平均報酬的統計值，非保證

## 模型實際看法(與下表顯示分數無關)
- 推高「上漲」最多：台積電(+0.51)、美元指數(+0.23)、投信5日買賣超(+0.07)、60日均線乖離(+0.05)、融資餘額變化(+0.02)
- 壓低「上漲」最多：費半(-1.15)、那斯達克(-0.33)、量比(-0.30)、當日漲跌(-0.24)、VIX水準(-0.21)

## 32 項因子
| # | 類別 | 因子 | 最新值 | 規則分數(-10~+10) | 模型貢獻 | 來源 |
|---|---|---|---|---|---|---|
| 1 | 籌碼 | 外資近5日買賣超(聯發科) | -6,212 張 | -5 | -0.05 | FinMind/模型 |
| 2 | 籌碼 | 投信近5日買賣超(聯發科) | 1,168 張 | +1 | +0.07 | FinMind/模型 |
| 3 | 籌碼 | 自營商近5日買賣超(聯發科) | 1,139 張 | +1 | +0.01 | FinMind/模型 |
| 4 | 籌碼 | 三大法人合計(依張數加總) | -3,905 張 | -3 | — | FinMind/模型 |
| 5 | 籌碼 | 外資持股比例變化 | 51.73%（5日 -0.46 個百分點） | -6 | -0.05 | FinMind/模型 |
| 6 | 籌碼 | 融資融券餘額變化 | 融資 12,316 張（5日 +7.36%）／融券 63 張（5日 +40.00%） | -5 | +0.03 | FinMind/模型 |
| 7 | 籌碼 | 成交量/20日均量 | 0.09x | +0 | -0.30 | 模型 |
| 8 | 技術 | 相對5/20/60日均線 | 2/3 條之上 | +3 | -0.13 | 模型 |
| 9 | 技術 | RSI(14) | 52.2 | +1 | +0.01 | 模型 |
| 10 | 技術 | KD與MACD | K=52, MACD柱=+0.72% | +2 | +0.00 | 模型 |
| 11 | 技術 | 布林通道位置 | +0.50 | +3 | -0.11 | 模型 |
| 12 | 技術 | 20日支撐/壓力位置 | 83% (0=低點,100=高點) | -3 | -0.13 | 模型 |
| 13 | 國際 | 美股四大指數(前一美股日) | +0.85% / -0.50% / -1.48% / -7.88% | -3 | -0.38 | 模型 |
| 14 | 國際 | VIX恐慌指數 | 26.4 (-0.98%) | +1 | -0.19 | 模型 |
| 15 | 國際 | 那斯達克期貨(夜盤參考) | -2.55% | -9 | — | 僅參考 |
| 16 | 國際 | 美元指數/美債10年 | DXY -0.44% / 10Y -0.014 | +4 | +0.21 | 模型 |
| 17 | 國際 | 美元兌新台幣 | -0.32% | +5 | -0.02 | 模型 |
| 18 | 產業 | 費半與台積電 | SOX -7.88% / 台積電 +9.85% | +0 | -0.65 | 模型 |
| 19 | 產業 | 高通/博通/聯詠/瑞昱 | +0.00% / +0.00% / +1.04% / +4.20% | +2 | -0.12 | 模型 |
| 20 | 產業 | 手機/AI邊緣晶片需求 | 熱度 5 則｜博來積極佈局高階IPC應用市場；明年1月轉上櫃 - 台視全球資訊網（11/24） ｜ 今日漲停股｜限空令點火半導體與PCB強勢反彈，聯電、台玻、南亞亮燈鎖死1123｜豐雲學堂2026 年 11 月 - 永豐金證券（11/23） | +0 | — | 新聞關鍵字(粗略) |
| 21 | 產業 | 月營收與法說指引 | 熱度 13 則｜聯發科（2454）做什麼？Q3財報優於預期、股價反彈連攻漲停，AI ASIC成長動能完整解析｜豐雲學堂2026 年 11 月 - 永豐金證券（11/24） ｜ 【即時新聞】這幾檔零售股迎爆發！百思買(BBY)同店銷售創五年新高，目標百貨(TGT)業績狂飆 - CMoney（11/24） | +1 | — | 新聞關鍵字(粗略) |
| 22 | 產業 | Google(GOOGL)正規盤收盤漲跌 | +0.00% | +0 | +0.01 | 模型 |
| 23 | 產業 | Google(GOOGL)盤後最新價 | n/a（盤後資料取得失敗） | — | — | 即時(yfinance) |
| 24 | 產業 | Google TPU×聯發科新聞(中文) | 熱度 42 則｜聯發科有望受惠！Google砍博通TPU訂單百萬顆、2027年出貨量下修20% - 鉅亨網（11/22） ｜ 再奪Google TPU大單！聯發科獲大摩高喊6188元目標價 前三季EPS衝47元 - Yahoo股市（11/22） | +0 | — | 新聞關鍵字(粗略) |
| 25 | 產業 | Google TPU 國際新聞(英文) | 熱度 33 則｜Google reportedly cuts Broadcom-designed TPU plans, eyes more MediaTek chips - Investing.com（11/20） ｜ Broadcom Plunges 11% as Google Reportedly Shifts TPU Orders to MediaTek, Overshadowing Goldman's $460 Target; Marvell Sinks 10% - 24/7 Wall St.（11/20） | +0 | — | 新聞關鍵字(粗略) |
| 26 | 產業 | Alphabet AI晶片/資本支出動態 | 熱度 13 則｜Google shifts some '27 high-end AI chip orders from Broadcom to MediaTek, Ming-Chi Kuo says - Seeking Alpha（11/20） ｜ Key facts: Alphabet raises AI capex; Search slows; FCF turns negative - TradingView（11/21） | +1 | — | 新聞關鍵字(粗略) |
| 27 | 總經 | 國際油價(WTI/布蘭特) | +2.01% / -0.87% | -1 | -0.15 | 模型 |
| 28 | 總經 | 烏俄戰爭進度 | 熱度 5 則｜俄烏戰爭歐洲入場・一｜抗衡美國與俄羅斯：意外的Game Changer？｜劉燕婷 - 方格子 - vocus（11/23） ｜ 俄烏戰爭未歇…估超過70萬俄軍陣亡 逾1000士兵輕生 - 世界新聞網（11/24） | +1 | — | 新聞關鍵字(粗略) |
| 29 | 總經 | 美伊(中東)局勢 | 熱度 29 則｜伊朗高調公開「地下飛彈城」內部 標語嗆美國：混蛋 - UDN（11/24） ｜ 【中東戰局】中東衝突，突傳大消息 - 鉅亨號（11/23） | -1 | — | 新聞關鍵字(粗略) |
| 30 | 總經 | 美中科技管制與關稅 | 熱度 40 則｜又批台灣「偷走」晶片生意，川普再喊晶片關稅200%：台灣業者全都要來美國。我們會拿回所有晶片生意/ 李忠謙 / 新聞 - 風傳媒（11/25） ｜ 美中休兵能延長？川普再揮關稅大棒恐衝擊陸專家點變數- 國際 - 中時新聞網（11/24） | -3 | — | 新聞關鍵字(粗略) |
| 31 | 總經 | 聯準會利率預期 | 熱度 16 則｜聯準會升息，突發大消息！美國財長公開發出警告 - 鉅亨號（11/24） ｜ Fed 12 月升息機率降至 88.6%！美元跌離 19 個月高點，BTC 重返 6 萬美元能站穩？ - 區塊客（11/23） | -1 | — | 新聞關鍵字(粗略) |
| 32 | 總經 | 外資券商目標價/評等 | 熱度 12 則｜台股狂飆3300點重返4萬！「發哥」連2根漲停鎖死 大摩6188元目標價藏玄機 - FTNN 新聞網（11/24） ｜ Google TPU風向變！博通跌倒、發哥吃飽？大咖法人有「異」見最新目標價、評等1次看- 上市櫃 - 旺得富理財網（11/23） | +1 | — | 新聞關鍵字(粗略) |
| | **模型合計** | 其他特徵(近期漲跌、加權指數等) | | | -0.38 | |
| | | 基準傾向(截距：訓練期上漲日 vs 下跌日) | | | -0.04 | |
| | | **合計 ln(上漲/下跌)** | | | **-2.38** | |

> 註：「新聞關鍵字」僅對標題做正負詞計數，非真正語意判斷，無歷史資料可回測，未納入模型；融資增加視為偏空僅為顯示用的經驗規則。分數為顯示用的規則化評價，模型權重由歷史資料估計。
> 時間說明：每日台北約 06:00 執行：美股為前一美股日完整收盤；美股盤後交易要到台北約 09:00 才結束，Google 盤後價為執行當下的最新價(yfinance 盤後資料可能延遲或缺漏)。
> 本報告僅供參考，不構成投資建議。