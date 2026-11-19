# 聯發科(2454) 每日日報
產生時間：2026-11-19 09:41 (台北)　資料日：2026-11-18　收盤：3940.0　模式：即時模式(手動)

## 次一交易日預測
- **上漲 42% ／ 盤整 13% ／ 下跌 44%** → 方向不明（上漲−下跌 -2 個百分點），信心：低
- 規則化因子加權均分(-10~+10；我訂的簡易規則，非模型輸出，與預測機率不同)：+0.8
- 模型輸入：37 個特徵(含法人籌碼)

## 樣本外回測(滾動式，不偷看未來)
- 回測天數：606；訓練視窗 500 日，每 20 日往前滾動
- 三分類命中率：**48.7%**(永遠猜最常見類別基準線：40.3%)
- 漲跌方向命中率(排除盤整日，共 493 天)：**61.7%**(永遠猜漲基準線：49.5%)
- 是否達成 90% 目標：**否**　(長期穩定的次日預測，超過 60% 就已非常罕見；若回測出現 90% 以上，應先懷疑資料洩漏或過擬合)

## 實盤追蹤(本腳本每日預測 vs 實際)
- 已驗證 18 天；三分類命中 44.4%；方向命中 47.1%(n=17)

- 已驗證 18 天；三分類命中 8/18（44%，純猜約 33%）。有明確方向（上漲與下跌機率差≥8 個百分點）且實際非盤整的判斷 15 次，命中 7 次（47%，95% 信賴區間 25%–70%；純猜約 50%）。樣本少時區間很寬，無法據此判斷模型好壞；紀錄也混有不同版本的模型。

## 聯發科新聞：今日 11/19（6 則報導 → 6 個事件）
- 11/19 09:23 台股開盤走弱再探底聯發科苦撐40K守不住- 證券（工商時報） https://news.google.com/rss/articles/CBMiX0FVX3lxTE1uYXh0THFOMGt5NE12OXpncWpwMjBGS2ZIekU3R29od3JVU2hENzdGdC11aDRHVWdjZHh3dlFsdzh2YVlsa19sazBfWFdIeVdFVUV2OTE2RGJjd1BSdHNB?oc=5
- 11/19 09:17 台達電噴5%、聯發科漲2%！台積電早盤跌15元拚翻紅 台股開低下殺408點摜破4萬點大關（Yahoo股市） https://news.google.com/rss/articles/CBMi3gNBVV95cUxQUGN1ZWR1RUpJa0FyMkx1aUpLczcteDVNQ0d5Mkd3Y2M2dlNDTUhLXzJNOTE4MGdkR2I0TnJXSHJvZFFfSjVabThnSW1vaXVrSTZUQ1dab3diX1VJOUVVQzJYNnNEMlNJbXVPMjFuZXNFN3ZpUmxOU0c4c29RZm00RXh0bWlzQ2dSZkhGUXFfQnoteElqeDZNdnh2WE1SU2xBc2RPOFFnd0g3SFctVkt0NzdSVXNacDlUNkV6X2hMaTBiN3loZ0d3Ym80NlphZkJPWVBkSkoyTV92RlZJSkRjN0dTQ1I1emdKXzZQSTFZemt1QU1zeHZpMkJpZWxiT3NjX3Jjdk91cW5PdEJCTlZETnNwN1c1d1MzWkJ6cWg5MU9ZRUZkdXhmcmhqQmdVd1h5VlV6VkNfUThiMm9iOXB2ZGdRWkxQOVVEeS1qakp1VzNyNXhGYTVUMTVVVC1pOTZVbnRmRHFBbFJaV2UyOXV1NHpUTmdscHBRVl82UnpYZTR6NDdsTTZNa0V4QURfZG16MmJ2TTF3Vnd6bG5ZcldfdE1jQlJfczRvNEZ3dVI2MXlNbE5DNTF1T2FoQ1RnSXMyS25fN3RqV3Y3OTlBcFVtcEZmczBET3dWUVZvX3l3?oc=5
- 11/19 08:37 國家隊買盤一夜翻倍！台積電、台達電、聯發科… 10大買賣超「2檔大轉彎」 - 上市櫃（旺得富理財網） https://news.google.com/rss/articles/CBMiakFVX3lxTE0yRFRXdXJJdjJlRE1mZDlZT2lkR0FRWVZtVlpPTVZZREszcDU0MG1hYndySC1xN3VrOF9YdTljVEsxek9fOEZZdFVtU3V2bkZOSDd3Q2xsZ25heW5JYkowcFZKZldLbFZKcVE?oc=5
- 11/19 08:12 《經濟》台灣新創躋身全球前20強 鴻海、聯發科等25家企業入列（富聯網） https://news.google.com/rss/articles/CBMiiAFBVV95cUxPQWUxQWl4U1JjSldGT0labjdQREp0ejRXV0l3MS16eHFsVG12aDY5WGh5WXBfQzhDS25kVUlrTlk2Z0xHbGtjQmI0c2F4LTNYOGcxWFVjNTh5M3BBVHE1RjdTb1o4ZFk3MmlKV25BNm5udXo2ZjBvbDIxZXJUWjhWcHVsSTdmaXkw?oc=5
- 11/19 08:00 旺宏慘賠48％想抱10年！聯發科賺57元卻想賣掉換0050 投資人勸先存本金（UDN） https://news.google.com/rss/articles/CBMiU0FVX3lxTFB4ekF4MEI1SWhlYlFFYlF2cm5LcG54d3h2RU5LTUgwRXh5SjlUeGhZTGFWYklGdnJEY2dJS3c4RjA0cFNkREstc0FEZ3Q0eURCcXZJ0gFYQVVfeXFMTkJKMGlSVFplaUlMZXVnZWdDSUdEWG1QdlNfemVIMUVvN1VlOFVMaldFUTNjNW5SWTllME1EeWdvOUpncEt2Wl9uU204RElpalI2M2Y4OFZMQg?oc=5
- 11/19 00:35 台積、聯發科 認購熱 | 權證特區 | 證券（經濟日報） https://news.google.com/rss/articles/CBMiWkFVX3lxTFBDa3ZFUDk0RkJIVm5RZEhibXR6MHN2bVJSTU1rcHQ2MFp0UVlIRUllV3JNYjluVnhTNDMtM1EzZGdvVDdFYVhIQ0I2ZnFDV1g2X25vUTdiOXJZQQ?oc=5
- 註：僅即時版（手動更新）顯示，不進預測模型；來源 Google News，只列標題含聯發科／發哥／2454／MediaTek 者，可能漏列，請自行判讀。

## 自上次執行以來的變化（排程版，2026-11-19 07:27）
- 預測機率：上漲 33%→42%（+9 個百分點）／盤整 10%→13%／下跌 57%→44%
- 規則分數變動較大：Google(GOOGL)正規盤收盤漲跌 +2→+0
- 新出現的新聞標題：
  - [烏俄] 澤連斯基望美中深圳會談對俄施壓結束戰爭 - 大紀元（11/19）
  - [烏俄] BBC：三方會談讓克宮先贏一局　普丁未必離勝利更近一步 - 三立新聞網SETN.com（11/18）
  - [烏俄] 蒲亭將與川、習三方閉門會談 歐洲憂烏克蘭被迫讓步 - 公視新聞（11/18）
  - [烏俄] 烏克蘭最大規模空襲！克里米亞大橋受損　俄攔截1336架無人機 | 國際 | CTWANT - CTWANT（11/17）
  - [烏俄] BBC：三方會談讓克宮先贏一局 普亭未必離勝利更近一步 - 世界新聞網（11/18）
  - [美伊] 美伊開戰9個月陷僵局！川普祭經濟封鎖賭時間 | 民視新聞網 - LINE TODAY（11/17）
  - [美伊] 美3航母集結 伊朗全面戒備 - 中國時報- 翻爆（11/17）
  - [美伊] 美軍再轟伊朗格什姆島 川普警告「髒彈」威脅(圖) - 亞洲 - - (移動版) - 看中国网（11/17）
  - [美中] 中美舉行貿易理事會首次會議，真正要命的東西，一樣都沒端上來 - 鉅亨號（11/17）
  - [聯準會] 「這檔」終於開花結果 爆量衝上漲停! - 口袋證券（11/18）
- 註：新聞不進預測模型，新聞本身不會改變上漲／下跌機率；機率的變化只來自股價、匯率、盤後價等市場資料。新聞請自行判讀。

## 方案比對：即時版 vs 標準版
- 已累積可比對交易日：**5/10**（共 9 次即時執行，同一天多次取機率平均；待驗證 2 筆）
- 滿 10 個交易日後顯示初步比對。任何時間手動執行都會被記錄。

## 即時行情(即時版預測已套用)
- Google(GOOGL)：正規盤收 282.34 → 最新 286.71（+1.55%，盤後，11/19 08:59 台北）
- 博通(AVGO)：正規盤收 354.07 → 最新 359.63（+1.57%，盤後，11/19 08:59 台北）
- 高通(QCOM)：正規盤收 159.83 → 最新 163.32（+2.18%，盤後，11/19 08:59 台北）
- 已套用：目前無可套用的即時資料
- 標準版預測(不含即時資料)：上漲 42% ／ 盤整 13% ／ 下跌 44%

## 參考價位(情境，以目前價位 3940.0 計)
- 上漲情境：4068.3（+3.26%）／盤整：3941.9（+0.05%）／下跌：3845.2（-2.41%）
- 機率加權預期價：**3952.6（+0.32%）**　※訓練期各類別平均報酬的統計值，非保證

## 模型實際看法(與下表顯示分數無關)
- 推高「上漲」最多：WTI油價(+0.23)、量比(+0.15)、道瓊(+0.12)、KD-K值(+0.12)、投信5日買賣超(+0.10)
- 壓低「上漲」最多：VIX水準(-0.24)、布蘭特油價(-0.23)、美元指數(-0.16)、20日漲跌(-0.11)、美債殖利率變化(-0.08)

## 32 項因子
| # | 類別 | 因子 | 最新值 | 規則分數(-10~+10) | 模型貢獻 | 來源 |
|---|---|---|---|---|---|---|
| 1 | 籌碼 | 外資近5日買賣超(聯發科) | -258 張 | +0 | +0.00 | FinMind/模型 |
| 2 | 籌碼 | 投信近5日買賣超(聯發科) | 1,585 張 | +1 | +0.10 | FinMind/模型 |
| 3 | 籌碼 | 自營商近5日買賣超(聯發科) | 904 張 | +1 | -0.04 | FinMind/模型 |
| 4 | 籌碼 | 三大法人合計(依張數加總) | 2,230 張 | +2 | — | FinMind/模型 |
| 5 | 籌碼 | 外資持股比例變化 | 52.13%（5日 -0.06 個百分點） | -1 | +0.00 | FinMind/模型 |
| 6 | 籌碼 | 融資融券餘額變化 | 融資 11,693 張（5日 -4.59%）／融券 33 張（5日 -31.25%） | +3 | -0.07 | FinMind/模型 |
| 7 | 籌碼 | 成交量/20日均量 | 1.35x | +3 | +0.15 | 模型 |
| 8 | 技術 | 相對5/20/60日均線 | 2/3 條之上 | +0 | +0.06 | 模型 |
| 9 | 技術 | RSI(14) | 48.0 | +0 | +0.03 | 模型 |
| 10 | 技術 | KD與MACD | K=69, MACD柱=+1.01% | +2 | +0.17 | 模型 |
| 11 | 技術 | 布林通道位置 | +0.14 | +1 | -0.01 | 模型 |
| 12 | 技術 | 20日支撐/壓力位置 | 70% (0=低點,100=高點) | -2 | -0.07 | 模型 |
| 13 | 國際 | 美股四大指數(前一美股日) | -1.11% / -0.23% / +0.42% / +0.10% | -1 | +0.20 | 模型 |
| 14 | 國際 | VIX恐慌指數 | 24.6 (-3.53%) | +2 | -0.19 | 模型 |
| 15 | 國際 | 那斯達克期貨(夜盤參考) | +1.02% | +4 | — | 僅參考 |
| 16 | 國際 | 美元指數/美債10年 | DXY +0.31% / 10Y -0.037 | +0 | -0.23 | 模型 |
| 17 | 國際 | 美元兌新台幣 | -0.16% | +2 | -0.01 | 模型 |
| 18 | 產業 | 費半與台積電 | SOX +0.10% / 台積電 +0.23% | +0 | -0.01 | 模型 |
| 19 | 產業 | 高通/博通/聯詠/瑞昱 | +0.00% / +0.00% / +0.44% / +2.37% | +1 | -0.04 | 模型 |
| 20 | 產業 | 手機/AI邊緣晶片需求 | 熱度 13 則｜神準搶地端AI商機，軟硬整合拓展應用 - 台視全球資訊網（11/18） ｜ Qualcomm Inc(QCOM)股票11月18日盤中下跌3.02%：原因全解讀 - TradingKey（11/18） | +0 | — | 新聞關鍵字(粗略) |
| 21 | 產業 | 月營收與法說指引 | 熱度 13 則｜5,072億的豪賭：聯發科10月營收月減，憑什麼喊出雲端AI晶片狂飆6倍？ - 理財周刊（11/17） ｜ 【12:37 即時新聞】聯發科(2454)盤中走強，權值買盤回流成焦點 - CMoney（11/17） | +0 | — | 新聞關鍵字(粗略) |
| 22 | 產業 | Google(GOOGL)正規盤收盤漲跌 | +0.00% | +0 | +0.01 | 模型 |
| 23 | 產業 | Google(GOOGL)盤後最新價 | n/a（盤後資料取得失敗） | — | — | 即時(yfinance) |
| 24 | 產業 | Google TPU×聯發科新聞(中文) | 熱度 34 則｜黃仁勳接班未定、Google TPU搶單！分析師點名聯發科「未來數年最大贏家」受矚「這檔」遭輝達風波衝擊仍奪成交王 - Yahoo股市（11/16） ｜ 熱門股／郭明錤估Google TPU訂單看到2029年！聯發科有望受惠翻紅走揚/ 產經 - 非凡新聞台（11/17） | +0 | — | 新聞關鍵字(粗略) |
| 25 | 產業 | Google TPU 國際新聞(英文) | 熱度 10 則｜Nvidia Succession in Limbo; Ming-Chi Kuo: Google TPU Visibility Extends Through 2029, MediaTek the Biggest Beneficiary - BigGo Finance（11/16） ｜ MediaTek’s Google TPU project revenue reportedly ramps in Q4 - NeoTeo（11/18） | +0 | — | 新聞關鍵字(粗略) |
| 26 | 產業 | Alphabet AI晶片/資本支出動態 | 熱度 13 則｜Who Reaches $100 Billion in TPU Revenue First, Alphabet or Broadcom? - 24/7 Wall St.（11/17） ｜ Alphabet Climbs 3% as NVIDIA's Leadership Shake-Up Puts Google's AI Chips in the Spotlight; Microsoft Gains 2%, Amazon Ticks Up - 24/7 Wall St.（11/12） | +1 | — | 新聞關鍵字(粗略) |
| 27 | 總經 | 國際油價(WTI/布蘭特) | -4.12% / -3.95% | +6 | -0.00 | 模型 |
| 28 | 總經 | 烏俄戰爭進度 | 熱度 15 則｜俄烏和談未解僵局 歐能源危機加深內部分歧 - 公視新聞（11/18） ｜ 俄烏和平談判再啟動 學者：安全保障、領土與停火分歧 妥協空間有限 - Rti 中央廣播電臺（11/17） | +1 | — | 新聞關鍵字(粗略) |
| 29 | 總經 | 美伊(中東)局勢 | 熱度 18 則｜美伊再度交火！伊朗擴襲科威特、巴林 美軍三航母集結中東 - 鉅亨網（11/18） ｜ APEC前夕第三艘航母抵達中東：美國對伊朗是封是打？｜劉燕婷 - 方格子 - Vocus（11/18） | -2 | — | 新聞關鍵字(粗略) |
| 30 | 總經 | 美中科技管制與關稅 | 熱度 13 則｜美中領導人今年頻繁會面 紐時：壁壘高築 - 經濟日報（11/18） ｜ 紐時分析：川習愈走愈近 美中經濟壁壘卻愈築愈高 - 世界新聞網（11/18） | -2 | — | 新聞關鍵字(粗略) |
| 31 | 總經 | 聯準會利率預期 | 熱度 12 則｜12月聯準會升息風暴來了？股市、匯市、美債走到十字路口- 國際 - 工商時報（11/18） ｜ 12月如果FOMC再升息，美股會跌？重返升息後歷史怎麼走？｜美股評析｜豐雲學堂2026 年 11 月 - 永豐金證券（11/17） | +0 | — | 新聞關鍵字(粗略) |
| 32 | 總經 | 外資券商目標價/評等 | 熱度 12 則｜台股4萬點保衛戰！杜金龍揭逃命波結束？曝光潛力族群逢低布局加碼好時機！《雅筑會客室》EP70｜杜金龍、張雅筑 - 永豐金證券（11/18） ｜ 外資法人對旺矽前景看法不一 大摩維持目標價8,000元 大和下調目標價 - 經濟日報（11/18） | -2 | — | 新聞關鍵字(粗略) |
| | **模型合計** | 其他特徵(近期漲跌、加權指數等) | | | -0.08 | |
| | | 基準傾向(截距：訓練期上漲日 vs 下跌日) | | | -0.02 | |
| | | **合計 ln(上漲/下跌)** | | | **-0.05** | |

> 註：「新聞關鍵字」僅對標題做正負詞計數，非真正語意判斷，無歷史資料可回測，未納入模型；融資增加視為偏空僅為顯示用的經驗規則。分數為顯示用的規則化評價，模型權重由歷史資料估計。
> 時間說明：每日台北約 06:00 執行：美股為前一美股日完整收盤；美股盤後交易要到台北約 09:00 才結束，Google 盤後價為執行當下的最新價(yfinance 盤後資料可能延遲或缺漏)。
> 本報告僅供參考，不構成投資建議。