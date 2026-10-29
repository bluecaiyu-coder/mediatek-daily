#!/usr/bin/env python3
"""聯發科(2454) 每日因子日報 + 次日走勢機率預測

流程：
1. 下載價格資料(yfinance)與三大法人買賣超(TWSE T86，累積成本地快取)
2. 計算技術/國際市場特徵，用「滾動式樣本外回測」誠實回報歷史命中率
3. 以最近 N 日資料訓練，輸出次一交易日 漲/盤整/跌 機率
4. 抓新聞標題做關鍵字情緒(僅供參考，無歷史可回測，不進模型)
5. 輸出 26 項因子表 reports/YYYY-MM-DD.md，並可推播 Telegram

用法：python mediatek_daily.py [--backfill 250]
"""
import argparse
import datetime as dt
import os
import time
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
import requests
import yfinance as yf
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# ----------------------------- 設定 -----------------------------
CODE = "2454"
FLAT_BAND = 0.005          # 漲跌幅 ±0.5% 以內視為盤整
TRAIN_WINDOW = 500         # 訓練視窗(交易日)
TEST_STEP = 20             # 回測每次往前滾動天數
MIN_INST_ROWS = 250        # 法人快取至少累積這麼多天才納入模型
UA = {"User-Agent": "Mozilla/5.0 (mediatek-daily)"}
TZ_TW = dt.timezone(dt.timedelta(hours=8))

TW = {"mtk": "2454.TW", "tsmc": "2330.TW", "twii": "^TWII",
      "novatek": "3034.TW", "realtek": "2379.TW"}
OVERSEAS = {"sp500": "^GSPC", "nasdaq": "^IXIC", "dow": "^DJI", "sox": "^SOX",
            "vix": "^VIX", "wti": "CL=F", "brent": "BZ=F", "dxy": "DX-Y.NYB",
            "us10y": "^TNX", "usdtwd": "TWD=X", "qcom": "QCOM", "avgo": "AVGO", "googl": "GOOGL",
            "nq": "NQ=F"}

NEWS_QUERIES = {
    "ukraine": "烏克蘭 俄羅斯 戰爭 停火",
    "iran": "美國 伊朗 衝突 中東",
    "uschina": "美中 晶片 管制 關稅",
    "fed": "聯準會 利率 降息 升息",
    "analyst": "聯發科 外資 目標價 評等",
    "revenue": "聯發科 營收 法說會 財測",
    "demand": "智慧型手機 出貨 AI 邊緣 晶片 需求",
    "g_tw": ("Google TPU 聯發科", "zh", 7),
    "g_en": ("Google TPU MediaTek", "en", 7),
    "g_ai": ("Alphabet Google AI chip TPU capex", "en", 7),
}
POS = ["停火", "和談", "談判", "降息", "上修", "調升", "買進", "看好", "創高", "利多",
       "大漲", "突破", "緩和", "達成協議", "優於預期", "強勁", "回溫", "增持", "樂觀"]
NEG = ["升級", "攻擊", "轟炸", "制裁", "禁令", "管制", "升息", "下修", "調降", "賣出",
       "看壞", "重挫", "大跌", "衝突", "封鎖", "利空", "衰退", "不如預期", "警告", "加徵", "關稅"]


POS_EN = ["surge", "beat", "record", "partnership", "win", "deal", "expand", "order", "growth",
          "boost", "raise", "upgrade", "strong", "launch", "ramp", "demand"]
NEG_EN = ["delay", "cut", "ban", "probe", "lawsuit", "downgrade", "miss", "slump", "shortage",
          "cancel", "antitrust", "fall", "weak", "halt", "concern"]
NEWS_ITEMS = {}

# ----------------------------- 工具函式 -----------------------------
def pc(x):
    return "n/a" if x is None or pd.isna(x) else f"{x * 100:+.2f}%"


def cls(r):
    return "up" if r > FLAT_BAND else "down" if r < -FLAT_BAND else "flat"


def clip_int(x):
    return int(np.clip(round(x), -10, 10))


def avg(*xs):
    xs = [x for x in xs if x is not None]
    return clip_int(np.mean(xs)) if xs else None


def zs(col, sign=1):
    """以最近一個值相對近 250 日標準差，轉成 -2~+2 分。"""
    s = col.dropna()
    if len(s) < 30:
        return None
    sd = s.tail(250).std()
    if not sd or pd.isna(sd):
        return None
    return clip_int(sign * s.iloc[-1] / sd * 5)


def rsi(c, n=14):
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def align_prior(series, idx):
    """對每個台股交易日 t，取『日期嚴格早於 t』的最新海外資料(避免偷看未來)。"""
    s = series.dropna()
    left = pd.DataFrame({"date": pd.to_datetime(idx).astype("datetime64[ns]")})
    right = pd.DataFrame({"date": pd.to_datetime(s.index).astype("datetime64[ns]"),
                          "v": s.values})
    m = pd.merge_asof(left, right, on="date", direction="backward",
                      allow_exact_matches=False)
    return pd.Series(m["v"].values, index=idx)


def align_level(series, idx, cutoffs):
    """對每個台股交易日，取『下一個台股交易日之前』最新的海外收盤價(嚴格早於 cutoff)。"""
    s_ = series.dropna()
    left = pd.DataFrame({"date": pd.to_datetime(cutoffs).astype("datetime64[ns]")})
    right = pd.DataFrame({"date": pd.to_datetime(s_.index).astype("datetime64[ns]"), "v": s_.values})
    m = pd.merge_asof(left, right, on="date", direction="backward", allow_exact_matches=False)
    return pd.Series(m["v"].values, index=idx)


def _session(ts):
    e = ts.tz_convert("America/New_York")
    lm = e.hour * 60 + e.minute
    return "盤中" if 570 <= lm < 960 else "盤前" if 240 <= lm < 570 else "盤後" if 960 <= lm < 1200 else "休市"


def fetch_afterhours(tk):
    """美股正規盤收盤價與最新盤後(含盤前)價，來源 yfinance 1 分鐘資料(prepost)。"""
    h = yf.Ticker(tk).history(period="5d", interval="1m", prepost=True)
    if h is None or h.empty:
        return None
    et = h.index.tz_convert("America/New_York")
    mins = np.asarray(et.hour * 60 + et.minute)
    reg = h[(mins >= 570) & (mins < 960)]  # 09:30~16:00 ET
    if reg.empty:
        return None
    reg_close, last_px = float(reg["Close"].iloc[-1]), float(h["Close"].iloc[-1])
    return {"reg_close": reg_close, "last": last_px, "move": last_px / reg_close - 1,
            "reg_date": reg.index[-1].tz_convert("America/New_York").date(),
            "ts": h.index[-1].tz_convert(TZ_TW), "session": _session(h.index[-1])}


# ----------------------------- 資料下載 -----------------------------
def download():
    tk = {**TW, **OVERSEAS}
    raw = yf.download(list(tk.values()), period="5y", auto_adjust=True,
                      progress=False, group_by="column", threads=True)
    inv = {v: k for k, v in tk.items()}

    def field(name):
        df = raw[name].copy()
        df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
        return df.rename(columns=inv)

    return field("Close"), field("High"), field("Low"), field("Volume")


# ----------------------------- 三大法人 (TWSE T86) -----------------------------
def _find(fields, exact, contains=()):
    for i, f in enumerate(fields):
        if f.strip() == exact:
            return i
    for i, f in enumerate(fields):
        if all(k in f for k in contains):
            return i
    return None


def _num(x):
    return int(str(x).replace(",", "").strip())


def fetch_t86(d):
    r = requests.get("https://www.twse.com.tw/rwd/zh/fund/T86",
                     params={"date": d.strftime("%Y%m%d"), "selectType": "ALL",
                             "response": "json"}, headers=UA, timeout=30)
    j = r.json()
    if j.get("stat") != "OK":
        print(f"[warn] TWSE T86 {d.date()} stat={j.get('stat')!r}")
        return None
    fl = j["fields"]
    i_f = _find(fl, "外陸資買賣超股數(不含外資自營商)", ("外", "買賣超"))
    i_t = _find(fl, "投信買賣超股數", ("投信", "買賣超"))
    i_d = _find(fl, "自營商買賣超股數", ("自營商", "買賣超"))
    for row in j["data"]:
        if row[0].strip() == CODE:
            return {"foreign": _num(row[i_f]), "trust": _num(row[i_t]),
                    "dealer": _num(row[i_d])}
    print(f"[warn] TWSE T86 {d.date()} 找不到代號 {CODE}")
    return None


def fetch_finmind(start):
    """FinMind 公開 API：一次取得個股三大法人買賣超(單位：股)。"""
    r = requests.get("https://api.finmindtrade.com/api/v4/data",
                     params={"dataset": "TaiwanStockInstitutionalInvestorsBuySell",
                             "data_id": CODE, "start_date": start},
                     headers=UA, timeout=60)
    j = r.json()
    if j.get("status") != 200 or not j.get("data"):
        print(f"[warn] FinMind status={j.get('status')} msg={j.get('msg')}")
        return None
    df = pd.DataFrame(j["data"])
    df["net"] = df["buy"] - df["sell"]
    m = {"Foreign_Investor": "foreign", "Investment_Trust": "trust",
         "Dealer_self": "dealer", "Dealer_Hedging": "dealer"}
    df["k"] = df["name"].map(m)
    df = df.dropna(subset=["k"])
    if df.empty:
        print(f"[warn] FinMind 名稱未對應，實際名稱：{sorted(set(j['data'][0:1] and [x['name'] for x in j['data']]))}")
        return None
    out = df.pivot_table(index="date", columns="k", values="net", aggfunc="sum")
    out.index = pd.to_datetime(out.index)
    return out.reindex(columns=["foreign", "trust", "dealer"])


def update_inst_cache(trading_dates, backfill):
    path = "data/inst_flow.csv"
    cache = (pd.read_csv(path, index_col=0, parse_dates=True)
             if os.path.exists(path) else
             pd.DataFrame(columns=["foreign", "trust", "dealer"]))
    cache.index = pd.to_datetime(cache.index)
    lookback = max(60, backfill, 1300 if len(cache) < 1000 else 0)
    want = [d for d in trading_dates[-lookback:] if d not in cache.index]
    if want:
        fm = None
        try:
            fm = fetch_finmind(min(want).strftime("%Y-%m-%d"))
        except Exception as e:
            print(f"[warn] FinMind 失敗: {e}")
        if fm is not None:
            cache = pd.concat([cache, fm[~fm.index.isin(cache.index)]])
            print(f"[info] FinMind 取得 {len(fm)} 天法人資料")
        else:  # 備援：證交所逐日抓，連續失敗 3 次就放棄
            fails = 0
            for d in list(reversed(want))[:20]:
                try:
                    row = fetch_t86(d)
                except Exception as e:
                    print(f"[warn] T86 {d.date()} 例外: {e}")
                    row = None
                if row:
                    cache.loc[d] = row
                    fails = 0
                else:
                    fails += 1
                    if fails >= 3:
                        break
                time.sleep(3)
    cache = cache.sort_index()
    cache.index.name = "date"
    cache.to_csv(path)
    print(f"[info] 法人快取共 {len(cache)} 天")
    return cache


FINMIND = "https://api.finmindtrade.com/api/v4/data"


def fetch_finmind_raw(dataset, start):
    r = requests.get(FINMIND, params={"dataset": dataset, "data_id": CODE,
                                      "start_date": start}, headers=UA, timeout=60)
    j = r.json()
    if j.get("status") != 200 or not j.get("data"):
        print(f"[warn] FinMind {dataset} status={j.get('status')} msg={j.get('msg')}")
        return None
    df = pd.DataFrame(j["data"])
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date").sort_index()


def update_chip_extra(asof):
    """外資持股比例(%)、融資餘額(張)、融券餘額(張)，快取於 data/chip_extra.csv。"""
    path = "data/chip_extra.csv"
    cols = ["foreign_ratio", "margin_bal", "short_bal"]
    cache = (pd.read_csv(path, index_col=0, parse_dates=True)
             if os.path.exists(path) else pd.DataFrame(columns=cols))
    cache.index = pd.to_datetime(cache.index)
    cache = cache.reindex(columns=cols).astype(float)
    start = ((asof - pd.Timedelta(days=1900)) if len(cache) < 1000
             else (cache.index.max() - pd.Timedelta(days=7))).strftime("%Y-%m-%d")
    plan = (("TaiwanStockShareholding", {"foreign_ratio": "ForeignInvestmentSharesRatio"}),
            ("TaiwanStockMarginPurchaseShortSale",
             {"margin_bal": "MarginPurchaseTodayBalance",
              "short_bal": "ShortSaleTodayBalance"}))
    parts = {}
    for ds, mapping in plan:
        try:
            raw = fetch_finmind_raw(ds, start)
        except Exception as e:
            print(f"[warn] FinMind {ds} 失敗: {e}")
            continue
        if raw is None:
            continue
        for name, src in mapping.items():
            if src in raw.columns:
                parts[name] = pd.to_numeric(raw[src], errors="coerce")
            else:
                print(f"[warn] {ds} 缺欄位 {src}，實際欄位：{list(raw.columns)}")
    if parts:
        new = pd.DataFrame(parts)
        new = new[~new.index.duplicated(keep="last")]
        cache = new.combine_first(cache)
    cache = cache.reindex(columns=cols).sort_index()
    cache.index.name = "date"
    cache.to_csv(path)
    print(f"[info] 籌碼補充快取共 {len(cache)} 天")
    return cache


# ----------------------------- 新聞情緒 (粗略) -----------------------------
def news_score(query, lang="zh", days=2):
    from email.utils import parsedate_to_datetime
    loc = ({"hl": "zh-TW", "gl": "TW", "ceid": "TW:zh-Hant"} if lang == "zh"
           else {"hl": "en-US", "gl": "US", "ceid": "US:en"})
    r = requests.get("https://news.google.com/rss/search",
                     params={"q": f"{query} when:{days}d", **loc}, headers=UA, timeout=30)
    items = ET.fromstring(r.content).findall(".//item")
    heat = len(items)  # 新聞熱度：期間內相關報導則數
    pos, neg = (POS, NEG) if lang == "zh" else (POS_EN, NEG_EN)
    rows = []
    for it in items[:30]:
        t = (it.findtext("title") or "").strip()
        try:
            d = parsedate_to_datetime(it.findtext("pubDate")).strftime("%m/%d")
        except Exception:
            d = ""
        rows.append((d, t, (it.findtext("link") or "").strip()))
    if not rows:
        return None, [], 0, []
    net = [sum(w in t.lower() for w in pos) - sum(w in t.lower() for w in neg) for _, t, _ in rows]
    amp = 0.5 + 0.5 * min(heat, 40) / 40  # 熱度越高，情緒分數放大越多
    return clip_int(np.mean(net) * 6 * amp), [f"{t}（{d}）" for d, t, _ in rows[:3]], heat, rows[:8]


# ----------------------------- 特徵工程 -----------------------------
def build_features(close, high, low, vol):
    idx = close["mtk"].dropna().index
    c, h, l, v = (close["mtk"].loc[idx], high["mtk"].loc[idx],
                  low["mtk"].loc[idx], vol["mtk"].loc[idx])
    f = pd.DataFrame(index=idx)
    f["ret1"], f["ret5"], f["ret20"] = c.pct_change(), c.pct_change(5), c.pct_change(20)
    for n in (5, 20, 60):
        f[f"ma{n}_gap"] = c / c.rolling(n).mean() - 1
    f["rsi14"] = rsi(c)
    macd = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
    f["macd_hist"] = (macd - macd.ewm(span=9, adjust=False).mean()) / c
    rsv = (c - l.rolling(9).min()) / (h.rolling(9).max() - l.rolling(9).min()) * 100
    k = rsv.ewm(alpha=1 / 3, adjust=False).mean()
    f["kd_k"], f["kd_diff"] = k, k - k.ewm(alpha=1 / 3, adjust=False).mean()
    m20, s20 = c.rolling(20).mean(), c.rolling(20).std()
    f["bb_pos"] = (c - m20) / (2 * s20)
    f["vol_ratio"] = v / v.rolling(20).mean()
    f["range_pos"] = (c - l.rolling(20).min()) / (h.rolling(20).max() - l.rolling(20).min())

    # 台股同日資料(台股收盤後已知)
    for key in ("tsmc", "twii", "novatek", "realtek"):
        r = close[key].dropna().pct_change()
        f[f"{key}_ret"] = r.reindex(idx).fillna(0)
    # 海外資料：每個台股交易日 r，取下一個台股開盤前最新的美股收盤(涵蓋兩日間所有美股交易日)
    today = pd.Timestamp(dt.datetime.now(TZ_TW).date())
    cuts = list(idx[1:]) + [max(today, idx[-1] + pd.Timedelta(days=1))]

    def lvl(key):
        return align_level(close[key], idx, cuts)

    for key in ("sp500", "nasdaq", "dow", "sox", "qcom", "avgo",
                "wti", "brent", "dxy", "usdtwd", "googl"):
        f[f"{key}_ret"] = lvl(key).pct_change().fillna(0)
    v_ = lvl("vix")
    f["vix"], f["vix_chg"] = v_, v_.pct_change()
    f["us10y_chg"] = lvl("us10y").diff()

    f["nxt"] = c.pct_change().shift(-1)
    return f, c


# ----------------------------- 模型與回測 -----------------------------
def make_model():
    return make_pipeline(StandardScaler(), LogisticRegression(C=0.05, max_iter=2000))


def proba(m, X):
    p = m.predict_proba(X)
    full = np.zeros((len(X), 3))
    full[:, m.classes_.astype(int)] = p
    return full


def walk_forward(data, cols, window):
    X, y = data[cols], data["y"].values
    rows = []
    for s in range(window, len(data), TEST_STEP):
        e = min(s + TEST_STEP, len(data))
        m = make_model().fit(X.iloc[s - window:s], y[s - window:s])
        p = proba(m, X.iloc[s:e])
        base = np.bincount(y[s - window:s], minlength=3).argmax()
        for k in range(e - s):
            rows.append((y[s + k], p[k].argmax(), p[k][2] > p[k][0], base))
    r = pd.DataFrame(rows, columns=["y", "pred", "up_side", "base"])
    nf = r[r.y != 1]
    return {
        "n": len(r),
        "acc": float((r.y == r.pred).mean()),
        "base_acc": float((r.y == r.base).mean()),
        "n_dir": len(nf),
        "dir_acc": float(((nf.y == 2) == nf.up_side).mean()) if len(nf) else float("nan"),
        "always_up": float((nf.y == 2).mean()) if len(nf) else float("nan"),
    }


FEAT_ZH = dict(x.split("=") for x in (
    "ret1=當日漲跌;ret5=5日漲跌;ret20=20日漲跌;ma5_gap=5日均線乖離;ma20_gap=20日均線乖離;ma60_gap=60日均線乖離;"
    "rsi14=RSI;macd_hist=MACD柱;kd_k=KD-K值;kd_diff=K減D;bb_pos=布林位置;vol_ratio=量比;range_pos=20日區間位置;"
    "tsmc_ret=台積電;twii_ret=加權指數;novatek_ret=聯詠;realtek_ret=瑞昱;sp500_ret=S&P500;nasdaq_ret=那斯達克;"
    "dow_ret=道瓊;sox_ret=費半;qcom_ret=高通;avgo_ret=博通;wti_ret=WTI油價;brent_ret=布蘭特油價;dxy_ret=美元指數;"
    "usdtwd_ret=美元兌台幣;googl_ret=Google股價;vix=VIX水準;vix_chg=VIX變化;us10y_chg=美債殖利率變化;"
    "foreign_5d=外資5日買賣超;trust_5d=投信5日買賣超;dealer_5d=自營商5日買賣超;"
    "foreign_ratio_chg5=外資持股比例變化;margin_chg5=融資餘額變化;short_chg5=融券餘額變化").split(";"))
MODEL_DRIVERS = {}
FACTOR_CONTRIB = {}
FACTOR_FEATS = {
    "外資近5日買賣超(聯發科)": ["foreign_5d"], "投信近5日買賣超(聯發科)": ["trust_5d"],
    "自營商近5日買賣超(聯發科)": ["dealer_5d"], "外資持股比例變化": ["foreign_ratio_chg5"],
    "融資融券餘額變化": ["margin_chg5", "short_chg5"], "成交量/20日均量": ["vol_ratio"],
    "相對5/20/60日均線": ["ma5_gap", "ma20_gap", "ma60_gap"], "RSI(14)": ["rsi14"],
    "KD與MACD": ["kd_k", "kd_diff", "macd_hist"], "布林通道位置": ["bb_pos"], "20日支撐/壓力位置": ["range_pos"],
    "美股四大指數(前一美股日)": ["dow_ret", "sp500_ret", "nasdaq_ret"], "VIX恐慌指數": ["vix", "vix_chg"],
    "美元指數/美債10年": ["dxy_ret", "us10y_chg"], "美元兌新台幣": ["usdtwd_ret"],
    "費半與台積電": ["sox_ret", "tsmc_ret"], "高通/博通/聯詠/瑞昱": ["qcom_ret", "avgo_ret", "novatek_ret", "realtek_ret"],
    "Google(GOOGL)正規盤收盤漲跌": ["googl_ret"], "國際油價(WTI/布蘭特)": ["wti_ret", "brent_ret"]}


def lean_label(p):
    d = float(p[2] - p[0])
    return ("明顯偏多" if d >= .20 else "略偏多" if d >= .08 else "方向不明" if d > -.08
            else "略偏空" if d > -.20 else "明顯偏空"), d

SCEN = {}
LIVE_QUOTES = []
RUN = {"mode": "scheduled", "label": "排程模式"}


def price_scenarios(data, window, p, px):
    """各情境價位 = 目前價位 × (1 + 訓練期該類別的平均次日報酬)；機率加權為期望值。"""
    d = data.tail(window)
    m = [float(d.loc[d["y"] == k, "nxt"].mean()) if (d["y"] == k).any() else 0.0 for k in (0, 1, 2)]
    er = float(np.dot(p, m))
    return {"rets": m, "px": [px * (1 + r) for r in m], "exp_r": er, "exp_px": px * (1 + er), "base": px}



def model_drivers(model, x_live, feat_cols, k=5):
    """各特徵對『上漲 vs 下跌』對數勝算的貢獻 = (係數差) × (標準化後數值)。"""
    sc_, lr = model.named_steps["standardscaler"], model.named_steps["logisticregression"]
    cl_ = list(lr.classes_.astype(int))
    if 0 not in cl_ or 2 not in cl_:
        return {}
    w = lr.coef_[cl_.index(2)] - lr.coef_[cl_.index(0)]
    con = pd.Series(w * (x_live.values[0] - sc_.mean_) / sc_.scale_, index=feat_cols).sort_values()
    fmt = lambda ser: [(FEAT_ZH.get(n, n), float(v)) for n, v in ser.items()]
    b = float(lr.intercept_[cl_.index(2)] - lr.intercept_[cl_.index(0)])
    return {"up": fmt(con.tail(k)[::-1]), "down": fmt(con.head(k)), "base": b,
            "contrib": con.to_dict(), "total": float(b + con.sum())}


# ----------------------------- 實盤預測追蹤 -----------------------------
def update_predictions(c, asof, p, write=True):
    path = "data/predictions.csv"
    cols = ["asof", "p_down", "p_flat", "p_up", "pred", "actual"]
    df = (pd.read_csv(path, dtype=object) if os.path.exists(path)
          else pd.DataFrame(columns=cols))
    nxt = c.pct_change().shift(-1)
    for i, row in df.iterrows():
        if pd.isna(row["actual"]) or row["actual"] == "":
            d = pd.Timestamp(row["asof"])
            if d in nxt.index and pd.notna(nxt[d]):
                df.at[i, "actual"] = cls(nxt[d])
    if write:
        df = df[df["asof"] != asof]
        names = ["down", "flat", "up"]
        df.loc[len(df)] = [asof, f"{p[0]:.4f}", f"{p[1]:.4f}", f"{p[2]:.4f}",
                           names[int(np.argmax(p))], np.nan]
        df.to_csv(path, index=False)
    done = df.dropna(subset=["actual"])
    if done.empty:
        return None
    acc = float((done["pred"] == done["actual"]).mean())
    nf = done[done["actual"] != "flat"]
    dir_acc = (float(((nf["actual"] == "up") ==
                      (nf["p_up"].astype(float) > nf["p_down"].astype(float))).mean())
               if len(nf) else None)
    return {"n": len(done), "acc": acc, "dir_acc": dir_acc, "n_dir": len(nf)}


# ----------------------------- 網頁儀表板 -----------------------------
import html as _html

CSS = """
:root{--bg:#f4f6f9;--card:#fff;--ink:#1c2024;--mute:#6b7280;--line:#e5e7eb;--up:#e5484d;--down:#2f9e5b;--flat:#9aa3af}
@media(prefers-color-scheme:dark){:root{--bg:#0f1115;--card:#171a21;--ink:#e8eaed;--mute:#9aa3af;--line:#262b36;--up:#ff6b6f;--down:#4cc38a;--flat:#6b7280}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 -apple-system,"Segoe UI","Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif}
.wrap{max-width:960px;margin:0 auto;padding:18px 14px 50px}.sub{color:var(--mute);font-size:13px}
h1{font-size:21px;margin:0}h2{font-size:16px;margin:0 0 12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;margin-bottom:14px}
.top{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;align-items:flex-end;margin-bottom:14px}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.big{font-size:34px;font-weight:700;line-height:1.2}.up{color:var(--up)}.down{color:var(--down)}.flat{color:var(--flat)}
.row{display:flex;align-items:center;gap:10px;margin:8px 0}.row b{width:44px;font-weight:600}.row i{width:48px;text-align:right;font-style:normal}
.bar{flex:1;height:12px;background:var(--line);border-radius:6px;overflow:hidden}.bar span{display:block;height:100%}
.gauge{position:relative;height:10px;border-radius:5px;margin:14px 6px 6px;background:linear-gradient(90deg,var(--down),var(--line),var(--up))}
.gauge u{position:absolute;top:-5px;width:6px;height:20px;border-radius:3px;background:var(--ink);transform:translateX(-3px)}
.chip{display:inline-block;padding:2px 9px;border-radius:99px;font-size:12px;margin:2px 4px 2px 0;font-weight:600}
.stats{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.stat{border:1px solid var(--line);border-radius:10px;padding:10px 12px}.stat small{color:var(--mute);display:block}.stat b{font-size:22px}
.tw{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:14px}
th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{color:var(--mute);font-weight:500;font-size:12px}
tr.g td{background:var(--bg);font-weight:600;font-size:13px}
.s{display:inline-block;min-width:34px;text-align:center;border-radius:8px;padding:1px 6px;font-weight:700}
.s2{background:rgba(229,72,77,.22);color:var(--up)}.s1{background:rgba(229,72,77,.10);color:var(--up)}.s0,.sn{background:var(--line);color:var(--mute)}
.m1{background:rgba(47,158,91,.12);color:var(--down)}.m2{background:rgba(47,158,91,.25);color:var(--down)}
.bd{font-size:11px;border:1px solid var(--line);border-radius:6px;padding:1px 6px;color:var(--mute);white-space:nowrap}
.note{color:var(--mute);font-size:12.5px;line-height:1.7}.warn{background:rgba(250,176,5,.15);border-radius:10px;padding:8px 12px;margin-bottom:14px;font-size:13px}
"""
_LBL = {"up": "漲", "flat": "盤", "down": "跌"}


def sclass(x):
    return "s2" if x >= 6 else "s1" if x >= 2 else "s0" if x > -2 else "m1" if x > -6 else "m2"


def _e(x):
    return _html.escape(str(x))


def render_html(asof, px, chg1, spark, p, top, conf, composite, F, bt, live, window,
                note, now, hist_path, sample=False):
    lean, net_ = lean_label(p)
    cl = "up" if net_ >= .08 else "down" if net_ <= -.08 else "flat"
    v = list(spark)
    lo, hi = min(v), max(v)
    pts = " ".join(f"{i * 316 / (len(v) - 1) + 2:.1f},{66 - (x - lo) / ((hi - lo) or 1) * 58:.1f}" for i, x in enumerate(v))
    spark_svg = (f'<svg viewBox="0 0 320 70" width="100%" height="70"><polyline fill="none" stroke="var(--{"up" if v[-1] >= v[0] else "down"})" '
                 f'stroke-width="2" points="{pts}"/></svg>')
    bars = "".join(
        f'<div class="row"><b>{n}</b><div class="bar"><span style="width:{q * 100:.0f}%;background:var(--{c_})"></span></div><i>{q * 100:.0f}%</i></div>'
        for n, q, c_ in (("上漲", p[2], "up"), ("盤整", p[1], "flat"), ("下跌", p[0], "down")))
    sc = [x for x in F if x[4] is not None]
    pos = sorted([x for x in sc if x[4] >= 3], key=lambda x: -x[4])[:4]
    neg = sorted([x for x in sc if x[4] <= -3], key=lambda x: x[4])[:4]
    chips = lambda L, k: "".join(f'<span class="chip {k}">{_e(x[2])} {x[4]:+d}</span>' for x in L) or '<span class="sub">無</span>'
    def fc(n):
        v_ = FACTOR_CONTRIB.get(n)
        return "—" if v_ is None else f'<span class="{"up" if v_ >= 0 else "down"}">{v_:+.2f}</span>'

    rows, g = [], None
    for i, grp, n, val, scr, src in F:
        if grp != g:
            g = grp
            rows.append(f'<tr class="g"><td colspan="6">{_e(grp)}</td></tr>')
        chip = f'<span class="s {sclass(scr)}">{scr:+d}</span>' if scr is not None else '<span class="s sn">—</span>'
        rows.append(f"<tr><td>{i}</td><td>{_e(n)}</td><td>{_e(val)}</td><td>{chip}</td><td>{fc(n)}</td><td><span class='bd'>{_e(src)}</span></td></tr>")
    if MODEL_DRIVERS:
        rows.append('<tr class="g"><td colspan="6">模型合計（對數勝算 ln(上漲 / 下跌)）</td></tr>')
        for lab_, v_ in (("其他特徵（近期漲跌、加權指數等）", FACTOR_CONTRIB.get("__other__", 0.0)),
                         ("基準傾向（截距：訓練期上漲日 vs 下跌日）", MODEL_DRIVERS["base"]),
                         ("合計", MODEL_DRIVERS["total"])):
            rows.append(f'<tr><td></td><td>{lab_}</td><td></td><td></td><td><b class="{"up" if v_ >= 0 else "down"}">{v_:+.2f}</b></td><td></td></tr>')
    stats = ""
    if bt:
        ok = bt["acc"] >= .9 or bt["dir_acc"] >= .9
        stats = (f'<div class="card"><h2>樣本外回測（滾動式，不偷看未來）</h2><div class="stats">'
                 f'<div class="stat"><small>漲跌方向命中率</small><b>{bt["dir_acc"] * 100:.1f}%</b><small>永遠猜漲：{bt["always_up"] * 100:.1f}%</small></div>'
                 f'<div class="stat"><small>三分類命中率</small><b>{bt["acc"] * 100:.1f}%</b><small>基準線：{bt["base_acc"] * 100:.1f}%</small></div>'
                 f'<div class="stat"><small>回測天數</small><b>{bt["n"]}</b><small>訓練視窗 {window} 日</small></div>'
                 f'<div class="stat"><small>達成 90% 目標</small><b>{"是" if ok else "否"}</b><small>超過 60% 已屬罕見</small></div></div>'
                 f'<p class="note">只有「高於基準線」才代表模型有價值。回測若出現 90% 以上，應先懷疑資料洩漏或過擬合。</p></div>')
    if live:
        da = "n/a" if live["dir_acc"] is None else f'{live["dir_acc"] * 100:.1f}%'
        stats += (f'<div class="card"><h2>實盤追蹤（本系統每日預測 vs 實際）</h2><div class="stats">'
                  f'<div class="stat"><small>已驗證天數</small><b>{live["n"]}</b></div>'
                  f'<div class="stat"><small>方向命中率</small><b>{da}</b><small>n={live["n_dir"]}</small></div>'
                  f'<div class="stat"><small>三分類命中率</small><b>{live["acc"] * 100:.1f}%</b></div></div></div>')
    hist = ""
    if os.path.exists(hist_path):
        h = pd.read_csv(hist_path, dtype=object).tail(15).iloc[::-1]
        hr = []
        for _, r in h.iterrows():
            act = r["actual"] if isinstance(r["actual"], str) and r["actual"] else None
            mk = "待驗證" if act is None else ("✓" if act == r["pred"] else "✗")
            hr.append(f"<tr><td>{_e(r['asof'])}</td><td>{float(r['p_up']) * 100:.0f}% / {float(r['p_flat']) * 100:.0f}% / {float(r['p_down']) * 100:.0f}%</td>"
                      f"<td>{_LBL.get(r['pred'], '')}</td><td>{_LBL.get(act, '—')}</td><td>{mk}</td></tr>")
        if hr:
            hist = ('<div class="card"><h2>近期預測紀錄</h2><div class="tw"><table><tr><th>資料日</th><th>漲 / 盤 / 跌</th><th>預測</th><th>實際</th><th>結果</th></tr>'
                    + "".join(hr) + "</table></div></div>")
    gl = []
    for key, lab in (("g_tw", "中文"), ("g_en", "國際"), ("g_ai", "AI晶片")):
        for d_, t_, l_ in NEWS_ITEMS.get(key, [])[:5]:
            gl.append(f'<li><span class="bd">{lab}</span> <a href="{_e(l_)}" target="_blank" rel="noopener">{_e(t_)}</a> <span class="sub">{_e(d_)}</span></li>')
    gcard = ('<div class="card"><h2>Google / TPU 動態新聞</h2><ul style="padding-left:18px;margin:0;line-height:1.9">'
             + "".join(gl) + "</ul></div>") if gl else ""
    lcard = ""
    if LIVE_QUOTES:
        lr_ = "".join(
            f'<tr><td>{_e(q["name"])} <span class="sub">{_e(q["tk"])}</span></td><td>{q["reg_close"]:.2f}</td>'
            f'<td>{q["last"]:.2f}</td><td class="{"up" if q["move"] >= 0 else "down"}">{q["move"] * 100:+.2f}%</td>'
            f'<td>{_e(q["session"])}</td><td class="sub">{q["ts"]:%m/%d %H:%M}</td></tr>' for q in LIVE_QUOTES)
        lcard = ('<div class="card"><h2>即時行情（僅顯示，不影響預測模型）</h2><div class="tw"><table><tr><th>標的</th>'
                 '<th>正規盤收盤</th><th>最新價</th><th>漲跌</th><th>時段</th><th>時間（台北）</th></tr>' + lr_
                 + '</table></div><p class="note">資料來自 yfinance，可能延遲或缺漏；這些數字不會被餵進預測模型。</p></div>')
    scard = ""
    if SCEN:
        t_ = lambda n, k: f'<div class="stat"><small>{n}</small><b class="{k}">{SCEN["px"][{"up": 2, "flat": 1, "down": 0}[k]]:.1f}</b><small>{SCEN["rets"][{"up": 2, "flat": 1, "down": 0}[k]] * 100:+.2f}%</small></div>'
        scard = ('<div class="card"><h2>參考價位（情境，以目前價位 %.1f 計）</h2><div class="stats">' % SCEN["base"]
                 + t_("上漲情境", "up") + t_("盤整情境", "flat") + t_("下跌情境", "down")
                 + f'<div class="stat"><small>機率加權預期價</small><b>{SCEN["exp_px"]:.1f}</b><small>{SCEN["exp_r"] * 100:+.2f}%</small></div></div>'
                 + '<p class="note">各情境＝目前價位套用訓練期該類別的平均次日報酬；加權預期價為機率期望值。僅為統計平均，非保證。</p></div>')
    mcard = ""
    if MODEL_DRIVERS:
        ch = lambda L_, k_: "".join(f'<span class="chip {k_}">{_e(n)} {v:+.2f}</span>' for n, v in L_)
        mcard = ('<div class="card"><h2>模型實際看法（真正決定機率的因子）</h2><div class="sub">推高上漲機率</div>'
                 + ch(MODEL_DRIVERS["up"], "s1") + '<div class="sub" style="margin-top:6px">壓低上漲機率</div>'
                 + ch(MODEL_DRIVERS["down"], "m1")
                 + f'<p class="note">基準傾向（模型截距，反映訓練期上漲日與下跌日的比例）：{MODEL_DRIVERS.get("base", 0):+.2f}；各因子貢獻加上基準傾向 ＝ ln(上漲/下跌) ＝ {MODEL_DRIVERS.get("total", 0):+.2f}。與規則分數無關，兩者可能不一致。</p></div>')
    banner = '<div class="warn">⚠ 這是範例資料，僅供預覽版面，並非真實預測。</div>' if sample else ('<div class="warn">即時模式：下方「即時行情」僅供顯示，預測模型與排程版採同一套規則、不受即時資料影響；本次結果不列入實盤命中率追蹤。</div>' if RUN["mode"] == "live" else "")
    return f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>聯發科 2454 每日預測</title><style>{CSS}</style></head><body><div class="wrap">
<div class="top"><div><h1>聯發科 2454 · 每日預測儀表板</h1><div class="sub">資料日 {asof:%Y-%m-%d} ｜ 更新 {_e(now)}（台北）｜ 紅漲綠跌 ｜ {_e(RUN["label"])} ｜ <a href="index.html">排程版</a> · <a href="live.html">即時版</a></div></div>
<div style="text-align:right"><div class="big {'up' if chg1 >= 0 else 'down'}">{px:.1f}</div><div class="sub {'up' if chg1 >= 0 else 'down'}">{chg1 * 100:+.2f}%</div></div></div>{banner}
<div class="grid"><div class="card"><h2>下一交易日預測</h2><div class="big {cl}">{lean}</div><div class="sub">上漲 − 下跌 ＝ {net_ * 100:+.0f} 個百分點｜信心：{conf}</div>{bars}</div>
<div class="card"><h2>模型多空傾向</h2><div class="big {cl}">{net_ * 10:+.1f}</div><div class="gauge"><u style="left:{(net_ * 10 + 10) / 20 * 100:.0f}%"></u></div>
<div class="sub" style="display:flex;justify-content:space-between"><span>−10 偏空</span><span>+10 偏多</span></div><div class="note" style="margin-top:8px">＝（上漲機率 − 下跌機率）×10，由預測模型直接算出。表格「規則分數」的均分為 {composite:+.1f}，是我訂的簡易規則，不是模型輸出，兩者不同很正常。</div><div style="margin-top:10px">{spark_svg}<div class="sub">近 60 日收盤</div></div></div></div>
<div class="card"><h2>顯示分數最極端的因子（規則化評價，非模型）</h2><div class="sub">偏多</div>{chips(pos, "s1")}<div class="sub" style="margin-top:6px">偏空</div>{chips(neg, "m1")}</div>
{lcard}{scard}{mcard}{gcard}{stats}
<div class="card"><h2>{len(F)} 項因子明細</h2><div class="tw"><table><tr><th>#</th><th>因子</th><th>最新值</th><th>規則分數</th><th>模型貢獻</th><th>來源</th></tr>{"".join(rows)}</table></div>
<p class="note">分數為 −10（偏空）到 +10（偏多）的規則化評價，綜合分依來源加權（Google 類 1.5、新聞 0.5、其餘 1.0）；「新聞關鍵字」僅對標題做正負詞計數，無歷史可回測，不進模型。{_e(note)}</p></div>
{hist}
<p class="note">每日台北 08:30 更新：美股為前一美股日完整收盤，Google 另附盤後最新價；盤後價無歷史資料，無法回測。本頁僅供參考，不構成投資建議。</p></div></body></html>"""


# ----------------------------- 主程式 -----------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backfill", type=int, default=0, help="一次回補多少天法人資料")
    ap.add_argument("--mode", choices=["scheduled", "live"], default="scheduled",
                    help="scheduled=排程版(依設計推進)；live=手動即時版(納入全部最新資訊)")
    args = ap.parse_args()
    RUN["mode"] = args.mode
    RUN["label"] = "即時模式(手動)" if args.mode == "live" else "排程模式"
    live_mode = args.mode == "live"
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    close, high, low, vol = download()
    f, c = build_features(close, high, low, vol)
    asof = f.index[-1]

    # Google 盤後價：歷史無法回測，僅併入即時預測列(正規盤漲跌 × 盤後漲跌)
    googl_reg = float(f["googl_ret"].iloc[-1])
    ah = None
    try:
        ah = fetch_afterhours("GOOGL")
    except Exception as e:
        print(f"[warn] GOOGL 盤後價失敗: {e}")
    gd = close["googl"].dropna()
    if not (ah and len(gd) and ah["reg_date"] == gd.index[-1].date()):
        ah = None
    ah_fresh = bool(ah and ah["ts"] > pd.Timestamp(f.index[-1]).tz_localize(TZ_TW) + pd.Timedelta(hours=13, minutes=30))
    if ah_fresh:
        f.loc[f.index[-1], "googl_ret"] = (1 + googl_reg) * (1 + ah["move"]) - 1
    if live_mode:  # 即時行情：僅供網頁顯示，完全不進模型
        for nm_, tk_ in (("Google", "GOOGL"), ("博通", "AVGO"), ("高通", "QCOM")):
            try:
                q_ = fetch_afterhours(tk_)
                if q_:
                    LIVE_QUOTES.append({"name": nm_, "tk": tk_, **q_})
            except Exception as e:
                print(f"[warn] {tk_} 即時行情失敗: {e}")

    # 法人籌碼：快取累積，量夠才進模型
    cache = update_inst_cache(list(f.index), args.backfill)
    inst_all = cache.astype(float) / 1000.0  # 股 -> 張
    roll = inst_all.rolling(5).sum()          # 以快取自身日期計算，不受最新一天尚未公布影響
    for k in ("foreign", "trust", "dealer"):
        f[f"{k}_5d"] = roll[k].reindex(f.index)
    inst_cols = ["foreign_5d", "trust_5d", "dealer_5d"]
    use_inst = f[inst_cols[0]].notna().sum() >= MIN_INST_ROWS
    # 即時預測列：最新一天法人資料若尚未公布，沿用最近一個可得值
    for col in inst_cols:
        if pd.isna(f[col].iloc[-1]):
            rs = roll[col.replace("_5d", "")].dropna()
            if len(rs):
                f.loc[f.index[-1], col] = rs.iloc[-1]

    # 外資持股比例、融資融券
    try:
        chip = update_chip_extra(asof)
    except Exception as e:  # 新增因子失敗時不拖垮整支腳本
        print(f"[warn] 籌碼補充資料失敗，略過: {e}")
        chip = pd.DataFrame(columns=["foreign_ratio", "margin_bal", "short_bal"],
                            index=pd.DatetimeIndex([])).astype(float)
    f["foreign_ratio_chg5"] = (chip["foreign_ratio"] - chip["foreign_ratio"].shift(5)).reindex(f.index)
    f["margin_chg5"] = chip["margin_bal"].pct_change(5, fill_method=None).reindex(f.index)
    f["short_chg5"] = chip["short_bal"].pct_change(5, fill_method=None).reindex(f.index)
    f = f.replace([np.inf, -np.inf], np.nan)  # 餘額為 0 會產生無限大，模型會報錯
    extra_cols = ["foreign_ratio_chg5", "margin_chg5", "short_chg5"]
    use_extra = all(f[c_].notna().sum() >= MIN_INST_ROWS for c_ in extra_cols)
    chip_chg = pd.DataFrame({
        "foreign_ratio_chg5": chip["foreign_ratio"] - chip["foreign_ratio"].shift(5),
        "margin_chg5": chip["margin_bal"].pct_change(5, fill_method=None),
        "short_chg5": chip["short_bal"].pct_change(5, fill_method=None)})
    chip_chg = chip_chg.replace([np.inf, -np.inf], np.nan)
    for col in extra_cols:  # 最新一天尚未公布時，即時預測列沿用最近可得值
        if pd.isna(f[col].iloc[-1]):
            rs = chip_chg[col].dropna()
            if len(rs):
                f.loc[f.index[-1], col] = rs.iloc[-1]

    base_cols = [x for x in f.columns if x not in ("nxt", *inst_cols, *extra_cols)]
    feat_cols = base_cols + (inst_cols if use_inst else []) + (extra_cols if use_extra else [])

    data = f.dropna(subset=feat_cols + ["nxt"]).copy()
    data["y"] = data["nxt"].map(cls).map({"down": 0, "flat": 1, "up": 2}).astype(int)
    window = min(TRAIN_WINDOW, int(len(data) * 0.6))
    bt = walk_forward(data, feat_cols, window) if len(data) > window + TEST_STEP else None

    live = make_model().fit(data[feat_cols].tail(window), data["y"].tail(window))
    x_live = f[feat_cols].iloc[[-1]].fillna(0)
    x_live = x_live.clip(lower=data[feat_cols].quantile(0.005), upper=data[feat_cols].quantile(0.995), axis=1)
    p = proba(live, x_live)[0]
    names = ["下跌", "盤整", "上漲"]
    top = names[int(np.argmax(p))]
    conf = "低" if p.max() < 0.45 else "中" if p.max() < 0.60 else "高"
    SCEN.update(price_scenarios(data, window, p, float(c.iloc[-1])))
    MODEL_DRIVERS.update(model_drivers(live, x_live, feat_cols))
    cb, used = MODEL_DRIVERS.get("contrib", {}), set()
    for nm_, ft_ in FACTOR_FEATS.items():
        fs_ = [x for x in ft_ if x in cb]
        if fs_:
            FACTOR_CONTRIB[nm_] = float(sum(cb[x] for x in fs_))
            used.update(fs_)
    FACTOR_CONTRIB["__other__"] = float(sum(v for k_, v in cb.items() if k_ not in used))
    live_stats = update_predictions(c, asof.strftime("%Y-%m-%d"), p, write=not live_mode)

    # 新聞
    news = {}
    for k, q in NEWS_QUERIES.items():
        try:
            news[k] = news_score(*(q if isinstance(q, tuple) else (q,)))
        except Exception as e:
            print(f"[warn] news {k}: {e}")
            news[k] = (None, [], 0, [])
        NEWS_ITEMS[k] = news[k][3]

    # nq 夜盤期貨
    nq_ret = close["nq"].dropna().pct_change()

    # ---- 26 項因子 ----
    last = f.iloc[-1]
    F = []

    def add(grp, name, val, score, src):
        F.append((len(F) + 1, grp, name, val, score, src))

    tot = (roll["foreign"] + roll["trust"] + roll["dealer"]).dropna()
    S = tot.tail(250).std() if len(tot) >= 30 else float("nan")

    def inst_score(v, raw=None):  # 三者共用同一把尺：張數越大，分數越極端，不會被小額反向買賣抵銷
        if pd.isna(v) or pd.isna(S) or not S:
            return None
        return clip_int(v / S * 5)

    for key, nm in (("foreign", "外資"), ("trust", "投信"), ("dealer", "自營商")):
        rs = roll[key].dropna()
        v = rs.iloc[-1] if len(rs) else float("nan")
        txt = "n/a"
        if len(rs):
            txt = f"{v:,.0f} 張"
            if rs.index[-1] < asof:
                txt += f"（資料至 {rs.index[-1]:%m/%d}）"
        add("籌碼", f"{nm}近5日買賣超(聯發科)", txt,
            inst_score(v, inst_all[key]), "FinMind" + ("/模型" if use_inst else "/累積中"))
    tv = tot.iloc[-1] if len(tot) else float("nan")
    tx = "n/a" if pd.isna(tv) else f"{tv:,.0f} 張" + (f"（資料至 {tot.index[-1]:%m/%d}）" if tot.index[-1] < asof else "")
    add("籌碼", "三大法人合計(依張數加總)", tx, inst_score(tv), "FinMind" + ("/模型" if use_inst else "/累積中"))

    def lastv(series):
        x = series.dropna()
        return x.iloc[-1] if len(x) else float("nan")

    src_x = "FinMind" + ("/模型" if use_extra else "/累積中")
    fr, frc = lastv(chip["foreign_ratio"]), lastv(chip_chg["foreign_ratio_chg5"])
    add("籌碼", "外資持股比例變化",
        "n/a" if pd.isna(fr) else f"{fr:.2f}%（5日 {frc:+.2f} 個百分點）",
        zs(f["foreign_ratio_chg5"]), src_x)
    mb, sb = lastv(chip["margin_bal"]), lastv(chip["short_bal"])
    add("籌碼", "融資融券餘額變化",
        "n/a" if pd.isna(mb) else
        f"融資 {mb:,.0f} 張（5日 {pc(lastv(chip_chg['margin_chg5']))}）／"
        f"融券 {sb:,.0f} 張（5日 {pc(lastv(chip_chg['short_chg5']))}）",
        zs(f["margin_chg5"], -1), src_x)
    vr = last["vol_ratio"]
    add("籌碼", "成交量/20日均量", f"{vr:.2f}x",
        clip_int(np.sign(last["ret1"]) * max(vr - 1, 0) * 10), "模型")
    add("技術", "相對5/20/60日均線",
        f"{sum(last[f'ma{n}_gap'] > 0 for n in (5, 20, 60))}/3 條之上",
        avg(*[zs(f[f"ma{n}_gap"]) for n in (5, 20, 60)]), "模型")
    r = last["rsi14"]
    rs_ = (r - 50) / 20 * 5 if 30 <= r <= 70 else (5 - (r - 70) / 30 * 10 if r > 70 else -5 + (30 - r) / 30 * 10)
    add("技術", "RSI(14)", f"{r:.1f}", clip_int(rs_), "模型")
    add("技術", "KD與MACD", f"K={last['kd_k']:.0f}, MACD柱={last['macd_hist']*100:+.2f}%",
        avg(zs(f["kd_diff"]), zs(f["macd_hist"])), "模型")
    b = last["bb_pos"]
    bb_ = 5 * b if abs(b) <= 1 else np.sign(b) * 5 - (b - np.sign(b)) * 5
    add("技術", "布林通道位置", f"{b:+.2f}", clip_int(bb_), "模型")
    rp = last["range_pos"]
    add("技術", "20日支撐/壓力位置", f"{rp*100:.0f}% (0=低點,100=高點)", clip_int((0.5 - rp) * 10), "模型")

    z4 = [zs(f[f"{k}_ret"]) for k in ("dow", "sp500", "nasdaq", "sox")]
    add("國際", "美股四大指數(前一美股日)",
        " / ".join(pc(last[f"{k}_ret"]) for k in ("dow", "sp500", "nasdaq", "sox")), avg(*z4), "模型")
    add("國際", "VIX恐慌指數", f"{last['vix']:.1f} ({pc(last['vix_chg'])})", zs(f["vix_chg"], -1), "模型")
    add("國際", "那斯達克期貨(夜盤參考)", pc(nq_ret.iloc[-1]), zs(nq_ret), "僅參考")
    add("國際", "美元指數/美債10年", f"DXY {pc(last['dxy_ret'])} / 10Y {last['us10y_chg']:+.3f}",
        avg(zs(f["dxy_ret"], -1), zs(f["us10y_chg"], -1)), "模型")
    add("國際", "美元兌新台幣", pc(last["usdtwd_ret"]), zs(f["usdtwd_ret"], -1), "模型")

    add("產業", "費半與台積電", f"SOX {pc(last['sox_ret'])} / 台積電 {pc(last['tsmc_ret'])}",
        avg(zs(f["sox_ret"]), zs(f["tsmc_ret"])), "模型")
    add("產業", "高通/博通/聯詠/瑞昱",
        " / ".join(pc(last[f"{k}_ret"]) for k in ("qcom", "avgo", "novatek", "realtek")),
        avg(*[zs(f[f"{k}_ret"]) for k in ("qcom", "avgo", "novatek", "realtek")]), "模型")

    def nrow(grp, name, key):
        sc, t, heat, _ = news[key]
        txt = (f"熱度 {heat} 則｜" + " ｜ ".join(t[:2])) if t else "無資料"
        add(grp, name, txt, sc, "新聞關鍵字(粗略)")

    nrow("產業", "手機/AI邊緣晶片需求", "demand")
    nrow("產業", "月營收與法說指引", "revenue")
    sd_g = f["googl_ret"].tail(250).std()
    add("產業", "Google(GOOGL)正規盤收盤漲跌", pc(googl_reg),
        clip_int(googl_reg / sd_g * 5) if sd_g else None, "模型")
    add("產業", "Google(GOOGL)盤後最新價",
        (f"收盤 {ah['reg_close']:.2f} → 最新 {ah['last']:.2f}（{pc(ah['move'])}，{ah['ts']:%m/%d %H:%M} 台北）"
         + ("" if ah_fresh else "【已反映於台股今日走勢，未計入預測】") if ah else "n/a（盤後資料取得失敗）"),
        clip_int(ah["move"] / sd_g * 5) if ah_fresh and sd_g else None, "即時(yfinance)")
    nrow("產業", "Google TPU×聯發科新聞(中文)", "g_tw")
    nrow("產業", "Google TPU 國際新聞(英文)", "g_en")
    nrow("產業", "Alphabet AI晶片/資本支出動態", "g_ai")
    add("總經", "國際油價(WTI/布蘭特)", f"{pc(last['wti_ret'])} / {pc(last['brent_ret'])}",
        avg(zs(f["wti_ret"], -1), zs(f["brent_ret"], -1)), "模型")
    nrow("總經", "烏俄戰爭進度", "ukraine")
    nrow("總經", "美伊(中東)局勢", "iran")
    nrow("總經", "美中科技管制與關稅", "uschina")
    nrow("總經", "聯準會利率預期", "fed")
    nrow("總經", "外資券商目標價/評等", "analyst")

    def wt(x):
        return 1.5 if x[2].startswith(("Google", "Alphabet")) else 0.5 if "新聞" in x[5] else 1.0

    sc_w = [(x[4], wt(x)) for x in F if x[4] is not None]
    composite = (sum(a * w for a, w in sc_w) / sum(w for _, w in sc_w)) if sc_w else 0.0

    # ---- 報告 ----
    now = dt.datetime.now(TZ_TW).strftime("%Y-%m-%d %H:%M")
    L = [f"# 聯發科(2454) 每日日報", f"產生時間：{now} (台北)　資料日：{asof.date()}　收盤：{c.iloc[-1]:.1f}　模式：{RUN['label']}", ""]
    L += ["## 次一交易日預測",
          f"- **上漲 {p[2]*100:.0f}% ／ 盤整 {p[1]*100:.0f}% ／ 下跌 {p[0]*100:.0f}%** → {lean_label(p)[0]}（上漲−下跌 {lean_label(p)[1]*100:+.0f} 個百分點），信心：{conf}",
          f"- 規則化因子加權均分(-10~+10；我訂的簡易規則，非模型輸出，與預測機率不同)：{composite:+.1f}",
          f"- 模型輸入：{len(feat_cols)} 個特徵" + ("(含法人籌碼)" if use_inst else f"(法人籌碼累積中：{len(cache)}/{MIN_INST_ROWS} 天)"),
          "", "## 樣本外回測(滾動式，不偷看未來)"]
    if bt:
        L += [f"- 回測天數：{bt['n']}；訓練視窗 {window} 日，每 {TEST_STEP} 日往前滾動",
              f"- 三分類命中率：**{bt['acc']*100:.1f}%**(永遠猜最常見類別基準線：{bt['base_acc']*100:.1f}%)",
              f"- 漲跌方向命中率(排除盤整日，共 {bt['n_dir']} 天)：**{bt['dir_acc']*100:.1f}%**(永遠猜漲基準線：{bt['always_up']*100:.1f}%)",
              f"- 是否達成 90% 目標：**{'是' if bt['acc'] >= .9 or bt['dir_acc'] >= .9 else '否'}**"
              "　(長期穩定的次日預測，超過 60% 就已非常罕見；若回測出現 90% 以上，應先懷疑資料洩漏或過擬合)"]
    else:
        L.append("- 資料量不足，無法回測")
    if live_stats:
        da = "n/a" if live_stats["dir_acc"] is None else f"{live_stats['dir_acc']*100:.1f}%"
        L += ["", "## 實盤追蹤(本腳本每日預測 vs 實際)",
              f"- 已驗證 {live_stats['n']} 天；三分類命中 {live_stats['acc']*100:.1f}%；方向命中 {da}(n={live_stats['n_dir']})"]
    if LIVE_QUOTES:
        L += ["", "## 即時行情(僅顯示，不影響模型)"] + [
            f"- {q['name']}({q['tk']})：正規盤收 {q['reg_close']:.2f} → 最新 {q['last']:.2f}"
            f"（{pc(q['move'])}，{q['session']}，{q['ts']:%m/%d %H:%M} 台北）" for q in LIVE_QUOTES]
    if SCEN:
        sn = SCEN
        L += ["", f"## 參考價位(情境，以目前價位 {sn['base']:.1f} 計)",
              f"- 上漲情境：{sn['px'][2]:.1f}（{sn['rets'][2]*100:+.2f}%）／盤整：{sn['px'][1]:.1f}（{sn['rets'][1]*100:+.2f}%）／下跌：{sn['px'][0]:.1f}（{sn['rets'][0]*100:+.2f}%）",
              f"- 機率加權預期價：**{sn['exp_px']:.1f}（{sn['exp_r']*100:+.2f}%）**　※訓練期各類別平均報酬的統計值，非保證"]
    if MODEL_DRIVERS:
        L += ["", "## 模型實際看法(與下表顯示分數無關)",
              "- 推高「上漲」最多：" + "、".join(f"{n}({v:+.2f})" for n, v in MODEL_DRIVERS["up"]),
              "- 壓低「上漲」最多：" + "、".join(f"{n}({v:+.2f})" for n, v in MODEL_DRIVERS["down"])]
    L += ["", f"## {len(F)} 項因子", "| # | 類別 | 因子 | 最新值 | 規則分數(-10~+10) | 模型貢獻 | 來源 |", "|---|---|---|---|---|---|---|"]
    for i, g, n, v, s, src in F:
        L.append(f"| {i} | {g} | {n} | {str(v).replace('|', '/')} | {'—' if s is None else f'{s:+d}'} | {'—' if n not in FACTOR_CONTRIB else format(FACTOR_CONTRIB[n], '+.2f')} | {src} |")
    if MODEL_DRIVERS:
        L += [f"| | **模型合計** | 其他特徵(近期漲跌、加權指數等) | | | {FACTOR_CONTRIB.get('__other__', 0):+.2f} | |",
              f"| | | 基準傾向(截距：訓練期上漲日 vs 下跌日) | | | {MODEL_DRIVERS['base']:+.2f} | |",
              f"| | | **合計 ln(上漲/下跌)** | | | **{MODEL_DRIVERS['total']:+.2f}** | |"]
    L += ["", "> 註：「新聞關鍵字」僅對標題做正負詞計數，非真正語意判斷，無歷史資料可回測，未納入模型；"
              "融資增加視為偏空僅為顯示用的經驗規則。分數為顯示用的規則化評價，模型權重由歷史資料估計。",
          "> 時間說明：每日台北 08:30 執行，美股為前一美股日完整收盤，Google 另附盤後最新價(yfinance 盤後資料可能延遲或缺漏)。",
          "> 本報告僅供參考，不構成投資建議。"]
    text = "\n".join(L)
    day = asof.strftime("%Y-%m-%d")
    for path in (["reports/live.md"] if live_mode else [f"reports/{day}.md", "reports/latest.md"]):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)
    try:
        os.makedirs("docs", exist_ok=True)
        note = (f"模型使用 {len(feat_cols)} 個特徵" + ("，含法人籌碼" if use_inst else "，法人籌碼累積中")
                + ("，含外資持股與融資融券。" if use_extra else "。"))
        page = render_html(asof, float(c.iloc[-1]), float(c.pct_change().iloc[-1]), c.tail(60), p, top, conf,
                           composite, F, bt, live_stats, window, note, now, "data/predictions.csv")
        with open("docs/live.html" if live_mode else "docs/index.html", "w", encoding="utf-8") as fh:
            fh.write(page)
    except Exception:
        import traceback
        tb = traceback.format_exc()
        print("[warn] 產生網頁失敗:\n" + tb)
        with open("docs/live.html" if live_mode else "docs/index.html", "w", encoding="utf-8") as fh:
            fh.write("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
                     "<body style='font-family:sans-serif;padding:20px;max-width:900px;margin:auto'><h2>網頁產生失敗</h2>"
                     f"<p>{_html.escape(now)}：報告檔 reports/*.md 仍已更新。請把下方錯誤文字貼給開發者：</p>"
                     f"<pre style='white-space:pre-wrap;background:#f4f4f4;padding:12px'>{_html.escape(tb)}</pre>")

    # ---- 推播(可選) ----
    tok, chat = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    if tok and chat:
        msg = "\n".join(L[:9])[:4000]
        try:
            requests.post(f"https://api.telegram.org/bot{tok}/sendMessage",
                          data={"chat_id": chat, "text": msg}, timeout=30)
        except Exception as e:
            print(f"[warn] telegram: {e}")


if __name__ == "__main__":
    main()
