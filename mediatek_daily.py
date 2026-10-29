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
            "us10y": "^TNX", "usdtwd": "TWD=X", "qcom": "QCOM", "avgo": "AVGO",
            "nq": "NQ=F"}

NEWS_QUERIES = {
    "ukraine": "烏克蘭 俄羅斯 戰爭 停火",
    "iran": "美國 伊朗 衝突 中東",
    "uschina": "美中 晶片 管制 關稅",
    "fed": "聯準會 利率 降息 升息",
    "analyst": "聯發科 外資 目標價 評等",
    "revenue": "聯發科 營收 法說會 財測",
    "demand": "智慧型手機 出貨 AI 邊緣 晶片 需求",
}
POS = ["停火", "和談", "談判", "降息", "上修", "調升", "買進", "看好", "創高", "利多",
       "大漲", "突破", "緩和", "達成協議", "優於預期", "強勁", "回溫", "增持", "樂觀"]
NEG = ["升級", "攻擊", "轟炸", "制裁", "禁令", "管制", "升息", "下修", "調降", "賣出",
       "看壞", "重挫", "大跌", "衝突", "封鎖", "利空", "衰退", "不如預期", "警告", "加徵", "關稅"]


# ----------------------------- 工具函式 -----------------------------
def pc(x):
    return "n/a" if x is None or pd.isna(x) else f"{x * 100:+.2f}%"


def cls(r):
    return "up" if r > FLAT_BAND else "down" if r < -FLAT_BAND else "flat"


def clip_int(x):
    return int(np.clip(round(x), -2, 2))


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
    return clip_int(sign * s.iloc[-1] / sd)


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
def news_score(query):
    url = "https://news.google.com/rss/search"
    r = requests.get(url, params={"q": query + " when:2d", "hl": "zh-TW",
                                  "gl": "TW", "ceid": "TW:zh-Hant"},
                     headers=UA, timeout=30)
    items = ET.fromstring(r.content).findall(".//item")[:15]
    titles = [(it.findtext("title") or "").strip() for it in items]
    if not titles:
        return None, []
    net = [sum(w in t for w in POS) - sum(w in t for w in NEG) for t in titles]
    return clip_int(np.mean(net) * 2), titles[:3]


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
    # 海外資料：只用「嚴格早於 t」的最新收盤
    for key in ("sp500", "nasdaq", "dow", "sox", "qcom", "avgo",
                "wti", "brent", "dxy", "usdtwd"):
        f[f"{key}_ret"] = align_prior(close[key].dropna().pct_change(), idx)
    f["vix"] = align_prior(close["vix"], idx)
    f["vix_chg"] = align_prior(close["vix"].pct_change(), idx)
    f["us10y_chg"] = align_prior(close["us10y"].diff(), idx)

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


# ----------------------------- 實盤預測追蹤 -----------------------------
def update_predictions(c, asof, p):
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


# ----------------------------- 主程式 -----------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backfill", type=int, default=0, help="一次回補多少天法人資料")
    args = ap.parse_args()
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    close, high, low, vol = download()
    f, c = build_features(close, high, low, vol)
    asof = f.index[-1]

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
    chip = update_chip_extra(asof)
    f["foreign_ratio_chg5"] = (chip["foreign_ratio"] - chip["foreign_ratio"].shift(5)).reindex(f.index)
    f["margin_chg5"] = chip["margin_bal"].pct_change(5, fill_method=None).reindex(f.index)
    f["short_chg5"] = chip["short_bal"].pct_change(5, fill_method=None).reindex(f.index)
    extra_cols = ["foreign_ratio_chg5", "margin_chg5", "short_chg5"]
    use_extra = all(f[c_].notna().sum() >= MIN_INST_ROWS for c_ in extra_cols)
    chip_chg = pd.DataFrame({
        "foreign_ratio_chg5": chip["foreign_ratio"] - chip["foreign_ratio"].shift(5),
        "margin_chg5": chip["margin_bal"].pct_change(5, fill_method=None),
        "short_chg5": chip["short_bal"].pct_change(5, fill_method=None)})
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
    p = proba(live, x_live)[0]
    names = ["下跌", "盤整", "上漲"]
    top = names[int(np.argmax(p))]
    conf = "低" if p.max() < 0.45 else "中" if p.max() < 0.60 else "高"
    live_stats = update_predictions(c, asof.strftime("%Y-%m-%d"), p)

    # 新聞
    news = {}
    for k, q in NEWS_QUERIES.items():
        try:
            news[k] = news_score(q)
        except Exception as e:
            print(f"[warn] news {k}: {e}")
            news[k] = (None, [])

    # nq 夜盤期貨
    nq_ret = close["nq"].dropna().pct_change()

    # ---- 26 項因子 ----
    last = f.iloc[-1]
    F = []

    def add(grp, name, val, score, src):
        F.append((len(F) + 1, grp, name, val, score, src))

    def inst_score(v, raw):
        s = raw.dropna()
        if len(s) < 20 or pd.isna(v):
            return None
        scale = s.abs().mean() * 5
        return clip_int(v / scale * 2) if scale else None

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
    sgn = np.sign(last["ret1"])
    add("籌碼", "成交量/20日均量", f"{vr:.2f}x",
        int(2 * sgn) if vr > 1.5 else int(sgn) if vr > 1.2 else 0, "模型")

    n_above = sum(last[f"ma{n}_gap"] > 0 for n in (5, 20, 60))
    add("技術", "相對5/20/60日均線", f"站上 {n_above}/3 條", {3: 2, 2: 1, 1: -1, 0: -2}[n_above], "模型")
    r = last["rsi14"]
    add("技術", "RSI(14)", f"{r:.1f}",
        2 if r < 30 else -1 if r < 45 else 0 if r < 55 else 1 if r < 70 else -1, "模型")
    add("技術", "KD與MACD", f"K={last['kd_k']:.0f}, MACD柱={last['macd_hist']*100:+.2f}%",
        (1 if last["kd_diff"] > 0 else -1) + (1 if last["macd_hist"] > 0 else -1), "模型")
    b = last["bb_pos"]
    add("技術", "布林通道位置", f"{b:+.2f}", -1 if b > 1 else 1 if b > 0.3 else 1 if b < -1 else -1 if b < -0.3 else 0, "模型")
    rp = last["range_pos"]
    add("技術", "20日支撐/壓力位置", f"{rp*100:.0f}% (0=低點,100=高點)", -1 if rp > 0.9 else 1 if rp < 0.1 else 0, "模型")

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
        sc, t = news[key]
        add(grp, name, " ｜ ".join(t[:2]) if t else "無資料", sc, "新聞關鍵字(粗略)")

    nrow("產業", "手機/AI邊緣晶片需求", "demand")
    nrow("產業", "月營收與法說指引", "revenue")
    add("總經", "國際油價(WTI/布蘭特)", f"{pc(last['wti_ret'])} / {pc(last['brent_ret'])}",
        avg(zs(f["wti_ret"], -1), zs(f["brent_ret"], -1)), "模型")
    nrow("總經", "烏俄戰爭進度", "ukraine")
    nrow("總經", "美伊(中東)局勢", "iran")
    nrow("總經", "美中科技管制與關稅", "uschina")
    nrow("總經", "聯準會利率預期", "fed")
    nrow("總經", "外資券商目標價/評等", "analyst")

    scores = [x[4] for x in F if x[4] is not None]
    composite = float(np.mean(scores)) if scores else 0.0

    # ---- 報告 ----
    now = dt.datetime.now(TZ_TW).strftime("%Y-%m-%d %H:%M")
    L = [f"# 聯發科(2454) 每日日報", f"產生時間：{now} (台北)　資料日：{asof.date()}　收盤：{c.iloc[-1]:.1f}", ""]
    L += ["## 次一交易日預測",
          f"- **上漲 {p[2]*100:.0f}% ／ 盤整 {p[1]*100:.0f}% ／ 下跌 {p[0]*100:.0f}%** → 傾向「{top}」，信心：{conf}",
          f"- 因子綜合分(26項平均，-2~+2，僅顯示用)：{composite:+.2f}",
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
    L += ["", "## 26 項因子", "| # | 類別 | 因子 | 最新值 | 分數(-2~+2) | 來源 |", "|---|---|---|---|---|---|"]
    for i, g, n, v, s, src in F:
        L.append(f"| {i} | {g} | {n} | {str(v).replace('|', '/')} | {'—' if s is None else f'{s:+d}'} | {src} |")
    L += ["", "> 註：「新聞關鍵字」僅對標題做正負詞計數，非真正語意判斷，無歷史資料可回測，未納入模型；"
              "融資增加視為偏空僅為顯示用的經驗規則。分數為顯示用的規則化評價，模型權重由歷史資料估計。",
          "> 時間差提醒：台北 20:00 時美股當日尚未開盤，美股資料為前一美股日收盤。",
          "> 本報告僅供參考，不構成投資建議。"]
    text = "\n".join(L)
    day = asof.strftime("%Y-%m-%d")
    for path in (f"reports/{day}.md", "reports/latest.md"):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)

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
