# 聯發科(2454) 每日日報
產生時間：2026-11-26 16:38 (台北)　資料日：2026-11-26　收盤：3705.0　模式：即時模式(手動)

## 次一交易日預測
- **上漲 31% ／ 盤整 12% ／ 下跌 58%** → 明顯偏空（上漲−下跌 -27 個百分點），信心：中
- 規則化因子加權均分(-10~+10；我訂的簡易規則，非模型輸出，與預測機率不同)：-0.3
- 模型輸入：37 個特徵(含法人籌碼)

## 樣本外回測(滾動式，不偷看未來)
- 回測天數：607；訓練視窗 500 日，每 20 日往前滾動
- 三分類命中率：**49.3%**(永遠猜最常見類別基準線：40.5%)
- 漲跌方向命中率(排除盤整日，共 496 天)：**61.5%**(永遠猜漲基準線：49.8%)
- 是否達成 90% 目標：**否**　(長期穩定的次日預測，超過 60% 就已非常罕見；若回測出現 90% 以上，應先懷疑資料洩漏或過擬合)

## 實盤追蹤(本腳本每日預測 vs 實際)
- 已驗證 23 天；三分類命中 47.8%；方向命中 50.0%(n=22)

- 已驗證 22 天；三分類命中 11/22（50%，純猜約 33%）。有明確方向（上漲與下跌機率差≥8 個百分點）且實際非盤整的判斷 19 次，命中 10 次（53%，95% 信賴區間 32%–73%；純猜約 50%）。樣本少時區間很寬，無法據此判斷模型好壞；紀錄也混有不同版本的模型。

## 聯發科新聞：今日 11/26（30 則報導 → 25 個事件）
- 11/26 16:31 Vivo X500 Series With 50MP Zeiss-Tuned Cameras, MediaTek Dimensity 9600 Pro SoC, 144Hz AMOLED Display Launched In India（ETV Bharat） https://news.google.com/rss/articles/CBMiwwFBVV95cUxOM3Y0TWpGVldIbXcxdjdQUTNUYVJiZjlUMEQ4dWVPS3UySTl6NktBMGhQUmFwazBwMUtMckhWRFJ6Yi1rbEJFM2lXRkpqWlg0UUF3dXlFZlFRZEhqVGRHbEltMGo0VURnaldQR05XX0diV1RHclR2WjBlLTgwWmdGeEZQazRHQlYxQi1ZMWx3bUlKLU1SVkJueXZ2TWNLUVBUTjNmcG5od3FsaDcyTzJBUldZMkxjSE8tMDlnWDBTbWJubm_SAcgBQVVfeXFMUFBfc01pVVpadHpNRFd1cnVwczZPZmJxcmQ4aHA4UTVQT2d5blZjQU91bDE4UW1oUzZVaEpuSERGWktER2lLTnVMNUhIdUgzMk5ac3V6OWNiSTdqbFprZXBTYzhjQXo0aWhXUS1TQzhDU2ctYy02VVZob05Oem5HcmxGN1JHMXpSaFg1R1RZNl9Mdm5fY3dQWVpBQmVOZVVFekVPNkxyNmNzRkxoN29nSDJHQktNeEJ1cjVraUhVZUhkSGdJMkhKOHU?oc=5
- 11/26 16:21 Vivo X500 launched in India with MediaTek Dimensity 9600M, 64MP ZEISS-powered periscope, 7,500mAh battery: price, specifications（×2：91Mobiles） https://news.google.com/rss/articles/CBMikwFBVV95cUxQVTlSci1ZVGVzbUticVRuSVFfd25Ed19zcFZWd0ZhdHNtZTFjd1JiS3lhT3g2WTBXcFFOZVpVNTAtSGUyNGtEMEtCcjYzbjVvcExOR2p6ZEszaldoSUhyVW1RMjJZcXdJRUJkSmxJN2NXVWdmY3l3WnhrcmxCVWRqMFp2c2pmcmJmc1dpUHJSRU92SlXSAZgBQVVfeXFMTW55aFlPQmdfaTVjLUxlS3ppQXNPNWw1Z0lNSmdWU1NHM2NWTTBjZmpMUTBMV19UZko4bFh1Zk9xLXg3X0hvc3ktcTdRYmpSU0ozbnE1UHFuanRoRkducHhxLXZYNXZ1TGNrdnR4cVlSS29QNDI3bHF5YWUtbUNESVlDdm5DaV9HY2t4MGRLOFA5VEQ5blBIQUw?oc=5
- 11/26 16:15 Vivo X500 Pro Max, Vivo X500 Pro and Vivo X500 Launched in India With Up to MediaTek Dimensity 9600 Pro C...（Gadgets 360） https://news.google.com/rss/articles/CBMivwFBVV95cUxQSERINnRGb3hLdUpnM1hwaUkzXy1maktZQkZOaUdwLVpRQ0Q5d3M0SjJHVTdCazlVN3JoYWhTQUdERVhZMWc1cVIxUzJJUU16eVF2SE5UVUcyaW1Hek5JQ1JYWmZfMXRvd3ppaXBLa1ZGQ3g5aUJqWVlVU0xhUFViSU1nNmg0SFFyUDBGdVJJX0JwcEJpUUNVWUR6UklQZnJaZFFzdVlmMThlZkNxaGpCVDFzeXl4ck1QbXlaVDRIONIBxAFBVV95cUxQQWlXQzBWRW1mdG1QS21oVzRYemRmTkFMUnRmTm5oMlFtYjl5VEN1U2JfRmhWdFZZdmdUS1dldmtnREhuaFRIQmJBUnJJNi0wNG04am1KZmV0THlrdTNfR2RlQVdnQ3FrS2RtamFGOFk1Z0RLRjhXOXhGemZDX3dETTJGMXhZb2dmQnJlb2VZMTdjMFM2eGdIelRPYjhuTWprcXZObEFyeS1WRFJSU3YweGpWRXlJWXFYMm5TcExwWFN6OERl?oc=5
- 11/26 15:56 2454 聯發科 - Google傳增單！聯發科昨跌停今反彈逾6%，能追嗎？ - 股市爆料同學會（CMoney） https://news.google.com/rss/articles/CBMiWEFVX3lxTFBVS0E1bnFGaGdPTnAwTUx1WVZZdUhoZXN3MHRCYzliWU1QWFg3UU9XVHBubXl1TzBWMENqV3FtV3BoQkhmYmVJWmRyVHB4WTdfVVZldk5GRHE?oc=5
- 11/26 14:48 聯發科 2454 週五收盤，觀察是否站回 EMA13（CMoney） https://news.google.com/rss/articles/CBMiWEFVX3lxTE41X0wtd0N1NHNNNF9FWnJzQWtIZG0xTWw0OFZITlpuZFF6NE9VWWxuUmQzRGI0bEh3U1VxWExPcjY0NmtkVVdIMTllbl9lc2otTUstY0dtbVQ?oc=5
- 11/26 14:06 2454 聯發科 - 明天加油 - 股市爆料同學會（×4：CMoney） https://news.google.com/rss/articles/CBMiWEFVX3lxTE1qa002WjhERjZtSDQ0QmNrSlAyTmhBT3Y5ZVlXVnE1blphOEo3bjdyOXZyNTgzMXByY1djcl9YWVFwbkFzMlZWQmZLN1NNS3JvdWFwYV8yUWc?oc=5
- 11/26 13:47 台股收盤強彈956點！聯發科領軍電子股反攻　台積電跌5元收2145元（NOWnews今日新聞） https://news.google.com/rss/articles/CBMiUkFVX3lxTE1xMDEzU2Q0bFphblRlM0JPQmVVclRXeHU5d0pDem81dDJpYW9XZVRQWXFKRzNkNEQzdzBQM2VzalBfellnaU5FeWFxeDZkeTYwTWfSAVJBVV95cUxNcTAxM1NkNGxaYW5UZTNCT0JlVXJUV3h1OXdKQ3pvNXQyaWFvV2VUUFlxSkczZDREM3cwUDNlc2pQX3pZZ2lORXlhcXg2ZHk2ME1n?oc=5
- 11/26 10:51 台股狂飆！聯發科領軍強彈，散熱強攻、光學氣勢如虹，「5檔PCB飆股」一堆人不知道（聚財網） https://news.google.com/rss/articles/CBMiTEFVX3lxTE93cmM2S1hlVm03VUd4QmpwSllJQ2tocFFwM0VtYVNIQU4tV0FaQ2lPVmdNV0NMcklaRFZrbHpiQXRzQ3NyYzYyLThIUFk?oc=5
- 11/26 10:32 AI ASIC 動能強勁，花旗維持聯發科買進評等目標價 6,800 元（TechNews 科技新報） https://news.google.com/rss/articles/CBMiqwFBVV95cUxNQ0l2dG9QNW9keGJybG1OclYtVDdUUURYRTFxUm5oMG9oOGtBQUJNT19xNjJlbUs4NWFQWlkyMjc4NWh1dThfTVNUTm8xU0pQMkxqbmkxTkM4eDNkeUp3c29xZ3YyT0hHZmtaTTlmOFNDZnF2Wm4yak5MbTRELUFRMVhHZzE3dmNrYWRVNDJhRU1wSHRUZU5oUjBTdF9CRHhreC1WRXFrcDhmTnM?oc=5
- 11/26 10:17 《半導體》聯發科AI ASIC業務爆發外資估2027年放量、2028雙箭齊發- 上市櫃（旺得富理財網） https://news.google.com/rss/articles/CBMiakFVX3lxTFBaU1J6QVBieFNaa3p3NXE0NTdyUHV6RDA5MmxEb0puZzZ2U3FUeDg5Ylg3ZTVOME82dHBDNTdnZXNpb1hUVEc2M0poMzk1Z3ZkSVl3UFlocGhGY1JoN2hpOFg3WjVpUE9IQnc?oc=5
- 11/26 09:57 Taiwan Stocks Stage V-Shaped Rebound, Surge 956 Points to Reclaim 39,000 Level as Delta Electronics, MediaTek Lead Electronics Heavyweights Higher（BigGo Finance） https://news.google.com/rss/articles/CBMidkFVX3lxTE5FQk1uRnFXUGtSSWI2c2JuSDA4Tzd2c0h5LVFDVjI4d2ZmczNIaVdKekJGR18ycVdxenIyRW5uQWR6akh6MkJOY1BBNzBYSEE3Yl9DRmJxcHVHMElOZ3dEQm1YX3ozdFFOTllvaExJX19xN1ZoMVE?oc=5
- 11/26 09:51 國家隊25日狂砸720億救台股！台積電獨吞527億、聯發科跌停照買 00981A、00403A遭反手調節（旺得富理財網） https://news.google.com/rss/articles/CBMiakFVX3lxTE1lWUJzaVJoT01MR05kTDNyRXZ6VFNlOG9RT2xwN2pNR1FxV0xPaTR4eWtjNVBTUm1MWXZpLVFqSW1aOXRXb3ZfQ25IYlhjcmREcGhBcVUxZDZyUDhzaHJfM2I4dUp5eHpDd0E?oc=5
- 11/26 09:22 聯發科、川湖領漲千金股台股早盤強彈千點收復39K 台積電還在掙扎- 證券（工商時報） https://news.google.com/rss/articles/CBMiX0FVX3lxTE1fVDVDV2xfTXdxQkE4ckNYSDc0a1dmQzdfUzVvc0J4d3ZobGQyQmNJQkVtdGpLX1ZqUC15LU5DTVlCbjFNeWdsWDNzcHdjMlM1ekRHT0dpb3AyNS1aZ1NR?oc=5
- 11/26 08:53 聯發科近4交易日2漲停2跌停！股民看傻眼：根本台股大怒神| 台股雜談| 股市（×2：UDN、udn） https://news.google.com/rss/articles/CBMiUkFVX3lxTE9pZXhqQnJNUXd0WkRnajNTSDdvZzZZNDhGblJKcEhNZTJsOEEtZ3E3dlJPVWc4V1laVzl2dHQ2ZHJlWXozNTBxQTFJU1JDYndxZ2c?oc=5
- 11/26 08:45 散戶崩潰！聯發科、台達電慘跌逾4成達人曝反彈逃命價- 財經（中時新聞網） https://news.google.com/rss/articles/CBMibkFVX3lxTE5sMk1KYkQycS1Od0FLV1ZBRlVRbEM3SkgwdURpRjFHRUk5S29yX1ZOMnpOTWoyVl9lMkpHVm5NX0VWc21SSWk4WWo3bkhFYnptZjc3YS1mTkN4YzNoTWJnMzVJM0dEemJDRTVOTGV3?oc=5
- 11/26 07:35 2454 聯發科 - 如果今天出現以下走勢： 1. 開盤由黑翻紅。 2.反一明顯... - 股市爆料同學會（CMoney） https://news.google.com/rss/articles/CBMiWEFVX3lxTFBHR2VEdTR4UVo4dnZhZFA1Yms4aktlRTVEQmJtQ3NMdGdYSElFR3p1QjZlZ0V3NGpJb3M2QUVHdk9scHkwaDZkOVFzdVpuVVd4dkwyTDdOb2U?oc=5
- 11/26 07:34 《投信買超8-4》聯鈞(717)、聯發科(690)、大成鋼(689)（富聯網） https://news.google.com/rss/articles/CBMiiAFBVV95cUxPMnA0OU1YQUh3RTBmc1FLMGR2Z3hzVVZPbmJKWWllTTFLX2ZRdy1nMmtYQWtKOTltcVUwVnVGS1RiUnFoSkdaSmtaQUFrTGhzcV9QakhEZWVWaEcyS3RicWY2dUFRTDkyeXh6TVI0b012S3p2T2RJMEtkSW9WcTVjOElBaDhaaGk4?oc=5
- 11/26 07:06 個股：皇翔(2545)11/25取得聯發科股票290張，每股平均價格3,679.29元（富聯網） https://news.google.com/rss/articles/CBMiiAFBVV95cUxNbVh4YXBmWGxrYVJyYUZBUFZBeVlpNm5zWWhkR2RuMWlpemxTUnFpZEVsMjd6M1RzaEw3aTl0ZFZoRUF4d0J1N25ra0JkVEdJa3lhTXRvalB0R2RTd09jRGpzMHl3dHZRQU1MYTRpN3VFSUNUQlAzS3lESTV4VGYtT3ZFT3BJVVhF?oc=5
- 11/26 06:58 K線煉金術3／買錯聯發科果斷認賠！ 千萬達人用2大停損紀律不讓小虧變大賠（鏡週刊Mirror Media） https://news.google.com/rss/articles/CBMiXkFVX3lxTE1PVjYweXNhcG45U3piYnlHR243RE5GVFNhZUxIaDA3eVFJUzFWTkM3WTNMaGFsUVQxVGxIQTYzQ1JGb3E2UFdfa1B3MC1QM0JVbUdWUXZQalRCRlNrUkE?oc=5
- 11/26 06:30 股災自救1／搶救套牢股別死守成本價 達人揭聯發科、台達電、正2減碼價位（鏡週刊Mirror Media） https://news.google.com/rss/articles/CBMiZkFVX3lxTFBxSEdURTV4M2ZYekJyNGthZXNGaFI1MDZwVTJtWWJObHVGQ05HVDlsSHA2MjRnYnJiV3k2elZ4ZW9TS2VsTW9lVWZJZk8wc3VSMDdZNk82T1pKSmVWaU9rN2hLeS1Zdw?oc=5
- 11/26 06:28 股災自救3／大型權值股不必急賣！ 分析師點名聯發科、台達電「1理由」不怕！（鏡週刊Mirror Media） https://news.google.com/rss/articles/CBMiZkFVX3lxTFBsa01IM0RFZTI2OEhVenNQeHl5ajRzWTFFQWV3Rk5SR1ZrNFc2MlZySG1rSndwZmVqaDRoWnVob1BDaFF6RVAzMVU5NHNkT1dKSXdYYnVlM2cxVVdyaHZrUGNlcFg3UQ?oc=5
- 11/26 03:00 台積CoWoS產能眾人搶分食！輝達同聯發科等ASIC業者相競法人預估數據揭端倪- 日報（工商時報） https://news.google.com/rss/articles/CBMiX0FVX3lxTE9Pd081eEtRSzBMNjZpbW9PUTN4UkkxOW10aWM0ZmFsUUg0WVlCVy1yenFuS3NOVEIyVnVQNEoyZldUVFJNR2psS1F6UlJvWWNMc3lmYXNodG1GX2ljVExv?oc=5
- 11/26 02:53 聯發科2027年不出手機旗艦SoC？ 官方闢謠：一定登場（DIGITIMES） https://news.google.com/rss/articles/CBMia0FVX3lxTFA1aEdEelNQX0k3NEl1Um5sMW1peF9KMWlZdkZPQXRIMkQtdU1pNkVCQlBvbmZsNWxabVhlVjFlWllycFJkSllKMHVmdUk2Wno0WnZua0U4bm1FVTFuRXQzTjZjaV9USngxV19z?oc=5
- 11/26 02:37 4萬點失而復得！聯發科、鴻海爬出地下室 台達電還在跌（聚財網） https://news.google.com/rss/articles/CBMiTEFVX3lxTFBlS0R1V1JZclJ1UmFnM2RWdHZPTDVsLTRIcnZ3eW9HSy1CVHhKejR0RzFZM0NtUHFobkZqVXR2X1NZbXVZai1qdVdWaTg?oc=5
- 11/26 02:03 台股漲778點　聯發科台達電收漲停（經濟日報） https://news.google.com/rss/articles/CBMiekFVX3lxTE5CN091TjA2RlBXWTVPdVc5RTFqakNZdnNnRkEwc0lfcUVwNFpEdnI3RmdSZl9iLUFqVkVDSDE4eXdHaFQ0ckFsd0Q4Yy0yWlpzQjhaUzBwRldVcks1bU9zZVFfYU0yRHVxc3p4SUw0c3JYTHk0MkN3WVd30gFfQVVfeXFMTUVCZGw1N2ZhbGlVQWtYbjVHVmw0WG5FTXZqbWFtbVR6N0JDNXdZTExEN2pVSW1vNWxoSEhqUUY1NFJEWTRhak40VFZ1bFhjVThscXM5OUxXbi1VZDNoYzA?oc=5
- 註：僅即時版（手動更新）顯示，不進預測模型；來源 Google News，只列標題含聯發科／發哥／2454／MediaTek 者，可能漏列，請自行判讀。

## 自上次執行以來的變化（排程版，2026-11-26 12:21）
- 預測機率：上漲 38%→31%（-7 個百分點）／盤整 13%→12%／下跌 49%→58%　※資料日已不同(新交易日)
- 規則分數變動較大：成交量/20日均量 -6→+1、VIX恐慌指數 -4→+2、Google(GOOGL)正規盤收盤漲跌 -5→+0、國際油價(WTI/布蘭特) -2→+3、費半與台積電 -4→+0、高通/博通/聯詠/瑞昱 +0→+4
- 新出現的新聞標題：
  - [烏俄] 俄烏戰爭歐洲入場・一｜抗衡美國與俄羅斯：意外的Game Changer？ - 香港01（11/26）
  - [美伊] 受中東戰事影響 英國明年首季能源價格上限上調26% - Now 新聞（11/26）
  - [美伊] 中東原油出口連周下滑，霍爾木茲海峽通行量僅剩正常水準49% - BigGo 財經（11/25）
  - [美伊] 全球哀號！外媒曝美伊戰爭釀史上規模最大石油斷供慘劇 - 自由時報（11/24）
  - [美伊] 華府祭新制裁 伊朗貨幣黑市匯率暴跌 - Rti 中央廣播電臺（11/24）
  - [美伊] 反制西方衛星封鎖伊朗研發一米高解析度雷達衛星- 科技新聞 - PChome Online新聞（11/24）
  - [美伊] 〈能源盤後〉荷姆茲海峽3艘船遇襲 原油漲逾2% 但供應過剩仍壓頂 - Yahoo 財經（11/24）
  - [美伊] 【梅花評論】從黑海到地中海：俄烏衝突外溢與中東安全合作的戰略考驗 - 梅花新聞網（11/24）
  - [美伊] 伊朗首席談判代表卡利巴夫：美未履行7條件前不談 卡達斡旋盼重啟美伊對話 - 蕃新聞（11/25）
  - [美伊] 沙烏地阿拉伯悄悄終結秘密協議，影響深遠 - 鉅亨號（11/26）
- 註：新聞不進預測模型，新聞本身不會改變上漲／下跌機率；機率的變化只來自股價、匯率、盤後價等市場資料。新聞請自行判讀。

## 方案比對：即時版 vs 標準版
- 已累積可比對交易日：**7/10**（共 12 次即時執行，同一天多次取機率平均；待驗證 1 筆）
- 滿 10 個交易日後顯示初步比對。任何時間手動執行都會被記錄。

## 即時行情(即時版預測已套用)
- Google(GOOGL)：正規盤收 272.95 → 最新 274.89（+0.71%，盤後，11/26 08:59 台北）
- 博通(AVGO)：正規盤收 300.49 → 最新 304.00（+1.17%，盤後，11/26 08:59 台北）
- 高通(QCOM)：正規盤收 168.61 → 最新 169.97（+0.81%，盤後，11/26 08:59 台北）
- 已套用：Google +0.00%→+0.71%、博通 +0.00%→+1.17%、高通 +0.00%→+0.81%
- 標準版預測(不含即時資料)：上漲 31% ／ 盤整 12% ／ 下跌 57%

## 參考價位(情境，以目前價位 3705.0 計)
- 上漲情境：3827.9（+3.32%）／盤整：3706.8（+0.05%）／下跌：3613.1（-2.48%）
- 機率加權預期價：**3690.2（-0.40%）**　※訓練期各類別平均報酬的統計值，非保證

## 模型實際看法(與下表顯示分數無關)
- 推高「上漲」最多：投信5日買賣超(+0.09)、60日均線乖離(+0.08)、布林位置(+0.08)、高通(+0.05)、5日漲跌(+0.05)
- 壓低「上漲」最多：布蘭特油價(-0.28)、VIX水準(-0.23)、20日漲跌(-0.13)、瑞昱(-0.12)、外資持股比例變化(-0.06)

## 32 項因子
| # | 類別 | 因子 | 最新值 | 規則分數(-10~+10) | 模型貢獻 | 來源 |
|---|---|---|---|---|---|---|
| 1 | 籌碼 | 外資近5日買賣超(聯發科) | -8,978 張（資料至 11/25） | -7 | -0.04 | FinMind/模型 |
| 2 | 籌碼 | 投信近5日買賣超(聯發科) | 1,520 張（資料至 11/25） | +1 | +0.09 | FinMind/模型 |
| 3 | 籌碼 | 自營商近5日買賣超(聯發科) | 408 張（資料至 11/25） | +0 | +0.00 | FinMind/模型 |
| 4 | 籌碼 | 三大法人合計(依張數加總) | -7,050 張（資料至 11/25） | -5 | — | FinMind/模型 |
| 5 | 籌碼 | 外資持股比例變化 | 51.48%（5日 -0.65 個百分點） | -8 | -0.06 | FinMind/模型 |
| 6 | 籌碼 | 融資融券餘額變化 | 融資 11,404 張（5日 -2.47%）／融券 31 張（5日 -6.06%） | +2 | -0.03 | FinMind/模型 |
| 7 | 籌碼 | 成交量/20日均量 | 1.12x | +1 | +0.05 | 模型 |
| 8 | 技術 | 相對5/20/60日均線 | 1/3 條之上 | -1 | +0.08 | 模型 |
| 9 | 技術 | RSI(14) | 46.2 | -1 | +0.02 | 模型 |
| 10 | 技術 | KD與MACD | K=46, MACD柱=+0.50% | +0 | -0.03 | 模型 |
| 11 | 技術 | 布林通道位置 | -0.15 | -1 | +0.08 | 模型 |
| 12 | 技術 | 20日支撐/壓力位置 | 53% (0=低點,100=高點) | +0 | +0.02 | 模型 |
| 13 | 國際 | 美股四大指數(前一美股日) | +0.00% / +0.00% / +0.00% / +0.00% | +0 | -0.01 | 模型 |
| 14 | 國際 | VIX恐慌指數 | 27.0 (-4.38%) | +2 | -0.19 | 模型 |
| 15 | 國際 | 那斯達克期貨(夜盤參考) | +0.26% | +1 | — | 僅參考 |
| 16 | 國際 | 美元指數/美債10年 | DXY +0.08% / 10Y +0.000 | +0 | -0.04 | 模型 |
| 17 | 國際 | 美元兌新台幣 | +0.15% | -2 | +0.01 | 模型 |
| 18 | 產業 | 費半與台積電 | SOX +0.00% / 台積電 -0.23% | +0 | -0.05 | 模型 |
| 19 | 產業 | 高通/博通/聯詠/瑞昱 | +0.00% / +0.00% / +4.33% / +4.43% | +4 | -0.06 | 模型 |
| 20 | 產業 | 手機/AI邊緣晶片需求 | 熱度 7 則｜英柏得科技以自主工業級存儲技術 深耕高階利基市場 - udn（11/26） ｜ 博來積極佈局高階IPC應用市場；明年1月轉上櫃 - 台視全球資訊網（11/24） | +1 | — | 新聞關鍵字(粗略) |
| 21 | 產業 | 月營收與法說指引 | 熱度 13 則｜聯發科（2454）做什麼？Q3財報優於預期，股價為什麼又跌停？，AI ASIC成長動能完整解析｜豐雲學堂2026 年 11 月 - 永豐金證券（11/25） ｜ 雲端營收翻倍 Google仍燒91億現金 - 短新聞SHOTNEWS（11/25） | +1 | — | 新聞關鍵字(粗略) |
| 22 | 產業 | Google(GOOGL)正規盤收盤漲跌 | +0.00% | +0 | -0.04 | 模型 |
| 23 | 產業 | Google(GOOGL)盤後最新價 | 收盤 272.95 → 最新 274.89（+0.71%，11/26 08:59 台北）（即時版預測已套用） | — | — | 即時(yfinance) |
| 24 | 產業 | Google TPU×聯發科新聞(中文) | 熱度 54 則｜聯發科有望受惠！Google砍博通TPU訂單百萬顆、2027年出貨量下修20% - 鉅亨網（11/22） ｜ 再奪Google TPU大單！聯發科獲大摩高喊6188元目標價 前三季EPS衝47元 - Yahoo股市（11/22） | -1 | — | 新聞關鍵字(粗略) |
| 25 | 產業 | Google TPU 國際新聞(英文) | 熱度 14 則｜Broadcom Plunges 11% as Google Reportedly Shifts TPU Orders to MediaTek, Overshadowing Goldman's $460 Target; Marvell Sinks 10% - 24/7 Wall St.（11/20） ｜ Google Said to Trim Broadcom TPU Orders for 2027, Shift Share Toward MediaTek - BigGo Finance（11/20） | +1 | — | 新聞關鍵字(粗略) |
| 26 | 產業 | Alphabet AI晶片/資本支出動態 | 熱度 13 則｜Google shifts some '27 high-end AI chip orders from Broadcom to MediaTek, Ming-Chi Kuo says - Seeking Alpha（11/20） ｜ Key facts: Alphabet raises AI capex; Search slows; FCF turns negative - TradingView（11/21） | +1 | — | 新聞關鍵字(粗略) |
| 27 | 總經 | 國際油價(WTI/布蘭特) | +0.31% / -4.28% | +3 | -0.29 | 模型 |
| 28 | 總經 | 烏俄戰爭進度 | 熱度 7 則｜【俄烏戰爭】烏軍重創克里米亞大橋，俄烏局部停火談判中斷 全球地緣政經動態（2026年第22期） - 鉅亨號（11/25） ｜ 美擱置將商業作為激勵手段促使俄停戰想法 對烏安全保障仍不明朗 - RFI（11/25） | +3 | — | 新聞關鍵字(粗略) |
| 29 | 總經 | 美伊(中東)局勢 | 熱度 24 則｜【中東戰局】美伊衝突，傳來大消息 - 鉅亨號（11/26） ｜ 沙特王儲將參加在美國舉行的20國集團峰會 - RFI（11/25） | -1 | — | 新聞關鍵字(粗略) |
| 30 | 總經 | 美中科技管制與關稅 | 熱度 27 則｜川普收緊晶片出口管制！亞洲資料中心消化算力找美買家/ 全球財經/ 全球 - UDN（11/25） ｜ 「關稅大砲」瞄準中國與越南 美國重塑全球貿易秩序、AI晶片成關鍵戰場 - CMoney投資網誌（11/25） | -5 | — | 新聞關鍵字(粗略) |
| 31 | 總經 | 聯準會利率預期 | 熱度 32 則｜美國經濟成長 4.3%、通膨還降不下來，聯準會還會降息嗎？-下午先生 - CMoney投資網誌（11/26） ｜ 新關稅提案添通膨壓力 Fed高利率恐更難退場 - 鉅亨網（11/26） | -1 | — | 新聞關鍵字(粗略) |
| 32 | 總經 | 外資券商目標價/評等 | 熱度 23 則｜AI ASIC 動能強勁，花旗維持聯發科買進評等目標價 6,800 元 - TechNews 科技新報（11/26） ｜ 大型權值股不必急賣！ 分析師點名聯發科、台達電「1理由」不怕！ - 三立新聞（11/26） | +1 | — | 新聞關鍵字(粗略) |
| | **模型合計** | 其他特徵(近期漲跌、加權指數等) | | | -0.10 | |
| | | 基準傾向(截距：訓練期上漲日 vs 下跌日) | | | -0.02 | |
| | | **合計 ln(上漲/下跌)** | | | **-0.62** | |

> 註：「新聞關鍵字」僅對標題做正負詞計數，非真正語意判斷，無歷史資料可回測，未納入模型；融資增加視為偏空僅為顯示用的經驗規則。分數為顯示用的規則化評價，模型權重由歷史資料估計。
> 時間說明：每日台北約 06:00 執行：美股為前一美股日完整收盤；美股盤後交易要到台北約 09:00 才結束，Google 盤後價為執行當下的最新價(yfinance 盤後資料可能延遲或缺漏)。
> 本報告僅供參考，不構成投資建議。