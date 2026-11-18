# 聯發科(2454) 每日日報
產生時間：2026-11-18 16:07 (台北)　資料日：2026-11-18　收盤：3940.0　模式：即時模式(手動)

## 次一交易日預測
- **上漲 42% ／ 盤整 13% ／ 下跌 45%** → 方向不明（上漲−下跌 -3 個百分點），信心：中
- 規則化因子加權均分(-10~+10；我訂的簡易規則，非模型輸出，與預測機率不同)：+0.6
- 模型輸入：37 個特徵(含法人籌碼)

## 樣本外回測(滾動式，不偷看未來)
- 回測天數：607；訓練視窗 500 日，每 20 日往前滾動
- 三分類命中率：**48.8%**(永遠猜最常見類別基準線：41.5%)
- 漲跌方向命中率(排除盤整日，共 494 天)：**61.7%**(永遠猜漲基準線：49.4%)
- 是否達成 90% 目標：**否**　(長期穩定的次日預測，超過 60% 就已非常罕見；若回測出現 90% 以上，應先懷疑資料洩漏或過擬合)

## 實盤追蹤(本腳本每日預測 vs 實際)
- 已驗證 18 天；三分類命中 44.4%；方向命中 47.1%(n=17)

- 已驗證 17 天；三分類命中 8/17（47%，純猜約 33%）。有明確方向（上漲與下跌機率差≥8 個百分點）且實際非盤整的判斷 14 次，命中 7 次（50%，95% 信賴區間 27%–73%；純猜約 50%）。樣本少時區間很寬，無法據此判斷模型好壞；紀錄也混有不同版本的模型。

## 聯發科新聞：今日 11/18（17 則報導 → 16 個事件）
- 11/18 13:55 Taiwan's ASIC trio draw returning buyers: Alchip Technologies hits limit-up, MediaTek reclaims NT$4,000, Global Unichip opens limit-down（BigGo Finance） https://news.google.com/rss/articles/CBMidkFVX3lxTE95VWxEaTZLT2tETGRzckpQMEVYWFhxbVVxcFJDTm56YWt3QXVheXVPNTZDMjFLZG5PYzNXWFJuTE5mTWE5eXowU2p1azJENUw4U2VTeWZjbjZmSVQ1WlZmWkFCTUtxYzlUMFJwVEFMSjhjUTFMYlE?oc=5
- 11/18 12:50 國家隊買超縮水近三分之二！聯發科、台達電、00406A獲加碼創意跌停仍遭賣15億 - 上市櫃（旺得富理財網） https://news.google.com/rss/articles/CBMiakFVX3lxTFBlU1ZXT3A5bHFZTW1vVzBvLUhmUWw1aW82cjFTX2xZdzdhVk83bUx3Mm0xaGdvOVJXSVQ3bGpORmIyZkM2QURhdEdPd3MtREJsb2otWnVCWHF0eWlLODVuWGhBU291OGJudWc?oc=5
- 11/18 12:25 Taiwan Stocks Slip Back Below 40,000 as TSMC, MediaTek Buck the Selloff with NT$92.7 Billion in Combined Turnover（BigGo Finance） https://news.google.com/rss/articles/CBMidkFVX3lxTFBRV3pyS3E5bzFhOUVGdnBYeXl3Z1VXVjVWRExLY3cyYmZzVENNNlZZUnc0Tkdic1lpTlhXSW5mcWFrMk9aSlFGYzhrTkpPZ0N0VWxSZmVzWFprbHdXSGdXajRabEVORTZvZHIyc2FreERhSm5TOEE?oc=5
- 11/18 12:07 台股重返4萬點短暫翻紅！「權值雙雄」股價強漲、聯發科一度看到4字頭 成交額合計狂飆927億元（Yahoo股市） https://news.google.com/rss/articles/CBMimwNBVV95cUxQZGNxdHBiWDhYdExLdVo2dURib0Q1OWh6dzlzNUZQQ19NZHRwSjNXNmhrcHZ2ZTUxSGVZRmVWeGU3bTkyb0hzd212eGxud0RGMUtxYlViNnc1ZVByb2puYm92cWRGQmQ0VS1FdkZzUlVlazMweWJpUkNvY2pvQzBORG1fUGRrRkRrWm1kOVRadlQxX0ZhM205NlUyMVZqQnBWelYtSkR2OUpEOUd1V3FueWRtTnhMNFlzaHN2cVBZemlUZGl0cmxDbF9KZV9sXzJHV1NVTlROc3ZManRQYUh6MEVhdnVoQzc0MXNJZEtrSTA1eVhtTUR1WVBaeThsOExsRGVldkJfc1FaeEYxck1mc24yVjNnN3ZFbHR2eXZpZGhJaFc0SmFpTUJQTk9JcjZjUkgzNC1tazd6UGcyeVpybnB6R19oSWtGNDhPWU5zSmYtdWhnalBaMHFLLVdDYjlXZnZMTGJqWUJnV1JBNnNUU18weGhJU1NmVDJuQm1lLXdpWWFsM0JFcU9HOFhqcXQyZ09jOEUzdnV1eW8?oc=5
- 11/18 10:17 MediaTek Google TPU ASIC: Q4 revenue reportedly ramps（NeoTeo） https://news.google.com/rss/articles/CBMijgFBVV95cUxOdmZZd3picjhrbnpiTUZjazlCcHNUbUk2VURUTDJiRHgwZmRrXzRDZzFMTEhDRTBPTW0tbTl3YTY2c09INFlQN2ZzYm8zV2pjZFdkY0U0blZMQlBESDdFaHgxZVdrdWlRcjExOVA2a3dILVpOeVByZHpkc09RNnp5Tm9WT0dVLTU3TGdDTjNB?oc=5
- 11/18 10:15 Taiwan Stocks Rebound From Losses; TAIEX Jumps 682 Points in Early Trading to Reclaim 41,000 Level, Led by MediaTek（BigGo Finance） https://news.google.com/rss/articles/CBMidkFVX3lxTE1EZ3JWb1V4LUttTE5CbFFxbkxucXhFSmFZcjlUbk1LNkRGdTltNTRJSjZmT0RjOGxHWEE0N3lpdnpaLWoxVnpIUTdJaWRIUlVqMzE1QkVmQWM2dG9IalNPbXJkNnA1T1c4UEQ3ZFFjVnJuYk1HSVE?oc=5
- 11/18 08:48 輝達營收報喜能救台股？南亞、世芯、聯發科…5檔獲法人點名矽晶圓、探針卡先避開- 上市櫃（旺得富理財網） https://news.google.com/rss/articles/CBMiakFVX3lxTE52SnREd3R5RzhzWXk2NU5VQm05NFA0U01rYTdfS0gzRm9VNHA3M1JCb2JtRTFJRVR2WU8ybmh5YnIwZmgxSFpnU0Vfb3k4VFFqSzJ6X20xTk42Z1VyRGFwRWh2VzhSV2pQQUE?oc=5
- 11/18 08:39 看好聯發科！第四季拉貨跳升 摩爾投顧蔡慶龍曝「關鍵數字」（Yahoo新聞） https://news.google.com/rss/articles/CBMi9wJBVV95cUxOWWdhLS1oUFRjQUczNVdRR1VoRERLT2lmTTF4NGZHRnpLYU5xNkh3d2h2MFJIZHg4QksyOHZwcTVtVENVSjQwNWdaTXRIZ0t4SDZnX3VCQ1pQdzdGenNDWTlIVHlOSzc4eDhfdkczTjhTSUV4ZnFOT1FRc0kxaGVGSXRXUmEtXzJ0ZW8yVm1sYk9PTGpXS3gxaUVqMXJabzVlNUVQVEJwVXpJOEk5V055WllBbnlIYVNLZmRmbEthXzFWZTJQTDBLRWgwQUx2Zi1HaTdlVkJndlo4eXJ5MVBaWENMN2JtcE5Wbm5nenZFd3hpQld0U3JZRTFmemFXT1ZiNnVKNVpLWWo1MWFjRnpuTGIwRDFFMHYyaHk2clhXOWdZRlY4SUtLQm5OUFRuTUlTWHF3Q3VIY1RIa2t1REpMelpqNV9Wclk4bzZWbzZuSEFETnZGWGZKSGRoMk5DYjZGVmt6d3J3bGZKV2tfQmpJZFpKOEZCYzg?oc=5
- 11/18 07:40 聯發科、研華全掰了！00962成分股洗牌「9進9出」 華城、鴻準、勤誠入列（Yahoo股市） https://news.google.com/rss/articles/CBMitgJBVV95cUxQVDNaTzh4Z0psR2J2N3Y0bldGTjJJOXdVWXV6R0VjUTByNjBxOERnazZya24xclZtWkFWR1NTSHJhcE9MdUltRkFreTZqVEZXRjU4OEZtUUVReU1DRjhLQmRZbUJJQldfYkY4dXhrOXdrRE5MaU5vVHhXWERQa2lseV9aZ3U2amJySzRfNVhlbnZ4V3R5M0QtX1Eyd1ZZZ1hQbEpEUFJOa2dKQi1SVGpURjhsSjlfajlQQlBqUG9neDFRR3ZFcUp0Nmd1VnhoYnY3YWtnRlVGaEYtTkZrdzJBSXBzWFc1QXRJOVBJUkVXTVhycFJWcFJ1TFBwQUx1ZkFjRzZZS1NVLWlicUNnaTQ3c0xoQUJaWDhDVDV3WHdqN05KWGE1ekpoRENHZEJ3cTF6SE4xSVJn?oc=5
- 11/18 07:34 《自營商買超45-28》大 成(25)、聯發科(349)、啟 碁(256)（富聯網） https://news.google.com/rss/articles/CBMiiAFBVV95cUxOLVRXXzNNc2MyT2ZPSnRPdFM2RVVOVDg2S1hSNEZYcHFQZWFEVHFnM2FtUF85UW9iOEZSTnM3Vl9LVXZzMGhweU9NYnBQSk9hVm0xdjQ3emtpNkQ3bWtCUFhtTFRjOVVBcG95ZXZNLUQtLXJ4Y2Z3RG5GcUtQdm1CazEwOERSd295?oc=5
- 11/18 07:17 熱門股／郭明錤估Google TPU訂單看到2029年！聯發科有望受惠翻紅走揚| 產經（非凡新聞台） https://news.google.com/rss/articles/CBMiX0FVX3lxTFBpQ3hIRlFXSVpFeGMzVzhDM0N4RmZweEVxU0Z0SEZfajBaTDJyeS1IQXh0eFpkOTNkZ0pLOW56QVFoZHRyR1VqUC1kVnhwZmpjS1VxUTROU0pldXJjLUww?oc=5
- 11/18 07:00 聯發科、國巨、聯電全遭剔除！高股息ETF00944成分股大換血 24檔新兵一次看（Yahoo股市） https://news.google.com/rss/articles/CBMiggNBVV95cUxNWE1qYjhFMG5kOXRlZ2NrNUs5NDZCMEowUWJ4dTg5SXdkZUZZaGEweFFrNlRla0FYM3RYa3NnZ0VzdmRZOG15b2UwU1FtcENZbjlsaVowZUxPOHNCNXZWRm1xZGhXLUNmaGJibTJVOEpXOE9iSW44QzlPNDRsSC0yN2R3T0JPUGUtbmNpdFZJNXg1ZzBwaVFXTGlFekpGZlhMLWNMdnRrcXZ1RmRNTEk3TFFRZlFiaDRxcm1WSVp5ME1mTXNQei1GeXBLSkpRazl6UERlb1p2b01KUWhQTmQxUTUtWW5weEIwUVNPdlJRaWVhODRTcWNVWF9KbEE3d1FsM21Db01IajJLTE1OVGp5UWg2TEdDRjdJMzhaaHd5UC05SFhvMkRwWUYxYXdHN0tsT0lBZy0tUnh4dDlyVFZIeE9GWG1aTThDNUFPREV3bHhNLUY2cDNtNmlOVFozaU1lbHpLRGlOcXg2UE9yN19OUXdUODFSUnN5ZFNVYnlnelJKUQ?oc=5
- 11/18 06:13 【即時新聞】聯發科宣布最新AI ASIC專案進展，預期2028年起貢獻實質營收動能（CMoney投資網誌） https://news.google.com/rss/articles/CBMikAFBVV95cUxOWk5EYk84WTFPZ3AydDR3S3o2MTFkOVkxVlhKdkoyVktKa1oxTTdJQk5zamhEczBLQXF0TlB3RmluelJJeXlnYUttVl9ZMWZhdHYyQ1B3R1dnVFdMMHpvQzVBOUJiWlYzZTZESUlsWlp3Ym9XRno1N0RjOUNXdWd1WTFyQUFTUE5DZlpGeHRLb0Y?oc=5
- 11/18 04:41 三大法人買賣超 – 外資買超(2383)台光電、(3653)健策，投信買超(2330)台積電、(2454)聯發科，法人合計賣超547.25億元（永豐金證券） https://news.google.com/rss/articles/CBMi3wRBVV95cUxOUTFhb2xBZ0ltT0lyZ05YX1pJOGR6YkRxZWRtbHJST3FiaklQeDBuREE3dnhjMlYyMmdJTHU5VmIyalJvSHRmcVdJbTBMVFFiMHlfYmw5V3VVd004Y2tOWjEtVWFESjFIekNVS1BhNU9jU1RCWUxmN0JrS3B3dVFvZ0g0bmxSTk1xQjBIRzhLdXpSVWxnYnRoVFRRSlZuck1mTm9wSDNTUFRMM2JOVDd6YmR6Wm5oY1lGYndKM2ZoNzRQU0NaVmFHeDRPbUphbDUtcUtMU1lCU0EyWlh3UGV5bG9hMlgzUWl2SWlSdkNqTUNMOVhqcnNNcnFMNjA5dm5jS1E5bTZ6dnFRTFFMQk9XMHFid1dUdS1TNkpMdm9fX3g4UWJabjNsQVduMVNmV2lBZkhjRHVkenU3eWZsR0kzdjMxaUxydHlsampBSUx6MVVGQ0phR01jcGRzemFCeE1lbHJZc204U1RHN2c2QlBSWm1ZN2NuYW9YWnQ1elVzWmlsTndSRlZKa2hXMWZZN1RicmJ4YnNUNU9Ia3J2d1l5VmxvQWVSSDJMeldBb3FKTlkxT1NoZWhmMG1YWUU0Z0RNQ3VPbjIwWnhHZ0J4dnVnMmZvY1hIbmZMMTJXTFNUUnBJODFiTklDYllyUmUzXzhjdVNmTTBla0xZZnQydzgtaklIM0xZdmQ5cEdGQW10U3hSVHdmaGhrSWdYSE11OXp2dDZ2QndsMG83dHlTYnB3ZXdXSkZ5d3BQQVNXRFBycmpZSzhsWDJ1emdvTUdDdjhnV2l1ZzN1cmJ3LUFoS3J3?oc=5
- 11/18 03:00 AI晶片採購預測「下修近3成」 SemiAnalysis砍聯發科TPU專案出貨預估- 日報（工商時報） https://news.google.com/rss/articles/CBMiX0FVX3lxTFB6YjhtVGxtd01tRS1UVFdTdGw3ajEzbDlXNzQzdldyMGhQcmJITkNJVDdCdk5ud19wUndkOGlSRC1NbDc4WHVrdXVXY3ZfbFV1c05RUGtscjlJUDdrWkJz?oc=5
- 11/18 01:47 2454 聯發科 - 最牛一輪／聯發科報喜台新64靚 - 股市爆料同學會（×2：CMoney、經濟日報） https://news.google.com/rss/articles/CBMiWEFVX3lxTE4xM3BWeGNZNEZqRzBHVk1WYXhqaGpBSDRGWVJDeWRvUk1YRkxpcTJISThEVzdsaGlKVDBiVEx3UkZqSlBqMUw1c1lOVzdrMmlRRm1QQ0RibkQ?oc=5
- 註：僅即時版（手動更新）顯示，不進預測模型；來源 Google News，只列標題含聯發科／發哥／2454／MediaTek 者，可能漏列，請自行判讀。

## 自上次執行以來的變化（排程版，2026-11-18 07:28）
- 預測機率：上漲 38%→42%（+4 個百分點）／盤整 8%→13%／下跌 55%→45%　※資料日已不同(新交易日)
- 規則分數變動較大：VIX恐慌指數 -6→+0、美股四大指數(前一美股日) -4→+0、美元兌新台幣 -2→+1、Google(GOOGL)正規盤收盤漲跌 -3→+0、布林通道位置 -1→+1、美元指數/美債10年 +0→-2
- 新出現的新聞標題：
  - [烏俄] 美國防部副部長： 俄羅斯還想打下去各方都必須做好持續衝突的準備| 國際 - Newtalk新聞（11/18）
  - [烏俄] 歐盟批俄無意和平談判 俄警告法軍赴烏祕援等同「直接參戰」 - 世界新聞網（11/18）
  - [烏俄] 俄羅斯總統普丁抵達深圳 - 鉅亨號（11/18）
  - [美伊] APEC前夕第三艘航母抵達中東：美國對伊朗是封是打？ - 香港01（11/18）
  - [美伊] 伊朗拒絕退讓！談判立場進一步強硬，美伊再度交火，科威特和巴林 - 群益期貨（11/18）
  - [美伊] 美軍第三艘航母抵達中東 美伊衝突再現升級風險 - 鉅亨網（11/18）
  - [美伊] 對伊大規模空襲箭在弦上？美3航艦罕見齊聚中東、兩棲突擊艦待命 - 自由軍武頻道（11/18）
  - [美伊] 伊朗「髒彈」襲華府？美媒爆伊朗「具體計劃」卻無實證- 國際 - 香港文匯報（11/18）
  - [美中] 紐時分析：川習愈走愈近 美中經濟壁壘卻愈築愈高 - 世界新聞網（11/18）
  - [美中] 習近平APEC喊話深化合作！承諾降關稅、開放中國製造業 川習會前美中貿易再添變數 - 鉅亨網（11/18）
- 註：新聞不進預測模型，新聞本身不會改變上漲／下跌機率；機率的變化只來自股價、匯率、盤後價等市場資料。新聞請自行判讀。

## 方案比對：即時版 vs 標準版
- 已累積可比對交易日：**5/10**（共 9 次即時執行，同一天多次取機率平均；待驗證 1 筆）
- 滿 10 個交易日後顯示初步比對。任何時間手動執行都會被記錄。

## 即時行情(即時版預測已套用)
- Google(GOOGL)：正規盤收 280.18 → 最新 283.67（+1.25%，盤後，11/18 08:59 台北）
- 博通(AVGO)：正規盤收 341.69 → 最新 351.50（+2.87%，盤後，11/18 08:59 台北）
- 高通(QCOM)：正規盤收 166.71 → 最新 170.62（+2.35%，盤後，11/18 08:52 台北）
- 已套用：Google +0.00%→+1.25%、博通 +0.00%→+2.87%、高通 +0.00%→+2.35%
- 標準版預測(不含即時資料)：上漲 40% ／ 盤整 14% ／ 下跌 45%

## 參考價位(情境，以目前價位 3940.0 計)
- 上漲情境：4068.3（+3.26%）／盤整：3941.9（+0.05%）／下跌：3845.2（-2.41%）
- 機率加權預期價：**3951.2（+0.28%）**　※訓練期各類別平均報酬的統計值，非保證

## 模型實際看法(與下表顯示分數無關)
- 推高「上漲」最多：量比(+0.18)、高通(+0.17)、WTI油價(+0.13)、KD-K值(+0.12)、投信5日買賣超(+0.12)
- 壓低「上漲」最多：VIX水準(-0.27)、美元指數(-0.13)、20日漲跌(-0.11)、布蘭特油價(-0.09)、Google股價(-0.08)

## 32 項因子
| # | 類別 | 因子 | 最新值 | 規則分數(-10~+10) | 模型貢獻 | 來源 |
|---|---|---|---|---|---|---|
| 1 | 籌碼 | 外資近5日買賣超(聯發科) | 302 張（資料至 11/17） | +0 | +0.01 | FinMind/模型 |
| 2 | 籌碼 | 投信近5日買賣超(聯發科) | 1,836 張（資料至 11/17） | +1 | +0.12 | FinMind/模型 |
| 3 | 籌碼 | 自營商近5日買賣超(聯發科) | 631 張（資料至 11/17） | +0 | -0.03 | FinMind/模型 |
| 4 | 籌碼 | 三大法人合計(依張數加總) | 2,770 張（資料至 11/17） | +2 | — | FinMind/模型 |
| 5 | 籌碼 | 外資持股比例變化 | 52.19%（5日 -0.01 個百分點） | +0 | +0.01 | FinMind/模型 |
| 6 | 籌碼 | 融資融券餘額變化 | 融資 11,472 張（5日 -4.74%）／融券 45 張（5日 -4.26%） | +3 | -0.05 | FinMind/模型 |
| 7 | 籌碼 | 成交量/20日均量 | 1.41x | +4 | +0.18 | 模型 |
| 8 | 技術 | 相對5/20/60日均線 | 2/3 條之上 | +0 | +0.06 | 模型 |
| 9 | 技術 | RSI(14) | 48.0 | +0 | +0.03 | 模型 |
| 10 | 技術 | KD與MACD | K=69, MACD柱=+1.01% | +2 | +0.17 | 模型 |
| 11 | 技術 | 布林通道位置 | +0.14 | +1 | -0.01 | 模型 |
| 12 | 技術 | 20日支撐/壓力位置 | 70% (0=低點,100=高點) | -2 | -0.07 | 模型 |
| 13 | 國際 | 美股四大指數(前一美股日) | +0.00% / +0.00% / +0.00% / +0.00% | +0 | -0.01 | 模型 |
| 14 | 國際 | VIX恐慌指數 | 25.5 (+0.00%) | +0 | -0.27 | 模型 |
| 15 | 國際 | 那斯達克期貨(夜盤參考) | +1.09% | +4 | — | 僅參考 |
| 16 | 國際 | 美元指數/美債10年 | DXY +0.26% / 10Y +0.000 | -2 | -0.14 | 模型 |
| 17 | 國際 | 美元兌新台幣 | -0.07% | +1 | -0.00 | 模型 |
| 18 | 產業 | 費半與台積電 | SOX +0.00% / 台積電 +0.23% | +0 | -0.02 | 模型 |
| 19 | 產業 | 高通/博通/聯詠/瑞昱 | +0.00% / +0.00% / +0.44% / +2.37% | +1 | +0.10 | 模型 |
| 20 | 產業 | 手機/AI邊緣晶片需求 | 熱度 11 則｜神準搶地端AI商機，軟硬整合拓展應用 - 台視全球資訊網（11/18） ｜ 意騰-KY（7749）前三季EPS 11.95元創高 Edge AI聲學與語音方案成長動能受矚 - 台灣好新聞（11/17） | +0 | — | 新聞關鍵字(粗略) |
| 21 | 產業 | 月營收與法說指引 | 熱度 10 則｜5,072億的豪賭：聯發科10月營收月減，憑什麼喊出雲端AI晶片狂飆6倍？ - 理財周刊（11/17） ｜ 輝達法說會／輝達董事會表態 無意讓黃仁勳重新出任執行長 / 鏡週刊 - LINE TODAY（11/18） | +1 | — | 新聞關鍵字(粗略) |
| 22 | 產業 | Google(GOOGL)正規盤收盤漲跌 | +0.00% | +0 | -0.08 | 模型 |
| 23 | 產業 | Google(GOOGL)盤後最新價 | 收盤 280.18 → 最新 283.67（+1.25%，11/18 08:59 台北）（即時版預測已套用） | — | — | 即時(yfinance) |
| 24 | 產業 | Google TPU×聯發科新聞(中文) | 熱度 37 則｜黃仁勳接班未定、Google TPU搶單！分析師點名聯發科「未來數年最大贏家」受矚「這檔」遭輝達風波衝擊仍奪成交王 - Yahoo股市（11/16） ｜ 熱門股／郭明錤估Google TPU訂單看到2029年！聯發科有望受惠翻紅走揚/ 產經 - 非凡新聞台（11/17） | +0 | — | 新聞關鍵字(粗略) |
| 25 | 產業 | Google TPU 國際新聞(英文) | 熱度 9 則｜Nvidia Succession in Limbo; Ming-Chi Kuo: Google TPU Visibility Extends Through 2029, MediaTek the Biggest Beneficiary - BigGo Finance（11/16） ｜ MediaTek Google TPU ASIC: Q4 revenue reportedly ramps - NeoTeo（11/18） | +0 | — | 新聞關鍵字(粗略) |
| 26 | 產業 | Alphabet AI晶片/資本支出動態 | 熱度 11 則｜Alphabet Doubled Cloud Revenue and Raised $62B Selling Its Own Stock - Global Data Center Hub（11/12） ｜ Alphabet Climbs 3% as NVIDIA's Leadership Shake-Up Puts Google's AI Chips in the Spotlight; Microsoft Gains 2%, Amazon Ticks Up - 24/7 Wall St.（11/12） | +1 | — | 新聞關鍵字(粗略) |
| 27 | 總經 | 國際油價(WTI/布蘭特) | -2.29% / -1.55% | +2 | +0.04 | 模型 |
| 28 | 總經 | 烏俄戰爭進度 | 熱度 9 則｜美國防部副部長： 俄羅斯還想打下去各方都必須做好持續衝突的準備/ 國際 - Newtalk新聞（11/18） ｜ 俄烏和平談判再啟動 學者：安全保障、領土與停火分歧 妥協空間有限 - Rti 中央廣播電臺（11/17） | +1 | — | 新聞關鍵字(粗略) |
| 29 | 總經 | 美伊(中東)局勢 | 熱度 22 則｜APEC前夕第三艘航母抵達中東：美國對伊朗是封是打？ - 香港01（11/18） ｜ 伊朗拒絕退讓！談判立場進一步強硬，美伊再度交火，科威特和巴林 - 群益期貨（11/18） | -1 | — | 新聞關鍵字(粗略) |
| 30 | 總經 | 美中科技管制與關稅 | 熱度 15 則｜紐時分析：川習愈走愈近 美中經濟壁壘卻愈築愈高 - 世界新聞網（11/18） ｜ 習近平APEC喊話深化合作！承諾降關稅、開放中國製造業 川習會前美中貿易再添變數 - 鉅亨網（11/18） | -2 | — | 新聞關鍵字(粗略) |
| 31 | 總經 | 聯準會利率預期 | 熱度 12 則｜黃金別急著下車！高盛看好再衝5600美元 點名這個時間點 - 自由財經（11/18） ｜ 高盛：聯準會緊縮壓抑，黃金創歷史新高恐需再等兩年 - 鏈新聞 ABMedia（11/18） | +0 | — | 新聞關鍵字(粗略) |
| 32 | 總經 | 外資券商目標價/評等 | 熱度 15 則｜目標價殺到7字頭！「探針卡測試大廠」喊2027營收成長50%、毛利率6成 外資卻降幅4.92% - Yahoo股市（11/17） ｜ 聯發科法說後八家外資搶喊讚 第二家 ASIC 客戶是誰？瑞銀提出二種可能 - 經濟日報（11/16） | +0 | — | 新聞關鍵字(粗略) |
| | **模型合計** | 其他特徵(近期漲跌、加權指數等) | | | -0.07 | |
| | | 基準傾向(截距：訓練期上漲日 vs 下跌日) | | | -0.02 | |
| | | **合計 ln(上漲/下跌)** | | | **-0.08** | |

> 註：「新聞關鍵字」僅對標題做正負詞計數，非真正語意判斷，無歷史資料可回測，未納入模型；融資增加視為偏空僅為顯示用的經驗規則。分數為顯示用的規則化評價，模型權重由歷史資料估計。
> 時間說明：每日台北約 06:00 執行：美股為前一美股日完整收盤；美股盤後交易要到台北約 09:00 才結束，Google 盤後價為執行當下的最新價(yfinance 盤後資料可能延遲或缺漏)。
> 本報告僅供參考，不構成投資建議。