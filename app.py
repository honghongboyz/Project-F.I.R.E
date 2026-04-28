import streamlit as st
import yfinance as yf
import pandas as pd
import json
import base64
from datetime import datetime, date, timedelta

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Project F.I.R.E",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700&family=Noto+Sans+TC:wght@400;500;700&display=swap');
:root {
  --bg:      #090d12;
  --card:    #0f1923;
  --border:  #1e3a4a;
  --cyan:    #00d4ff;
  --green:   #00e87a;
  --red:     #ff3a5c;
  --amber:   #ffb300;
  --purple:  #b388ff;
  --text:    #ddeef5;
  --muted:   #6a9aaa;
  --dim:     #2a4a5a;
}
html, body, [data-testid="stApp"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Noto Sans TC', sans-serif;
  font-size: 15px;
}
/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="block-container"] { padding: 1.2rem 1.5rem 2rem !important; }

/* Sidebar */
[data-testid="stSidebar"] { background: #060a0f !important; border-right: 1px solid var(--border) !important; }
[data-testid="stSidebar"] label { color: var(--muted) !important; font-size: 0.82rem !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stSidebar"] input, [data-testid="stSidebar"] select { background: var(--card) !important; border: 1px solid var(--border) !important; color: var(--cyan) !important; font-size: 1rem !important; border-radius: 6px !important; }

/* Inputs */
input, select { background: var(--card) !important; border: 1px solid var(--border) !important; color: var(--cyan) !important; font-size: 1rem !important; min-height: 44px !important; border-radius: 6px !important; }

/* Metrics */
[data-testid="stMetric"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; padding: 14px 16px !important; }
[data-testid="stMetricLabel"] { font-size: 0.78rem !important; color: var(--muted) !important; text-transform: uppercase; letter-spacing: 0.06em; }
[data-testid="stMetricValue"] { font-family: 'Share Tech Mono', monospace !important; font-size: 1.45rem !important; color: var(--cyan) !important; }
[data-testid="stMetricDelta"] { font-size: 0.82rem !important; }

/* Buttons */
.stButton button { background: var(--card) !important; border: 1px solid var(--cyan) !important; color: var(--cyan) !important; font-size: 0.9rem !important; min-height: 44px !important; border-radius: 8px !important; letter-spacing: 0.04em; transition: all 0.15s; }
.stButton button:hover { background: rgba(0,212,255,0.08) !important; }

/* Expander */
[data-testid="stExpander"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }
details summary { font-size: 0.9rem !important; color: var(--cyan) !important; padding: 4px 0 !important; }

/* Cards */
.card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 18px 20px; }
.card-red   { background: #140008; border: 2px solid var(--red);   border-radius: 12px; padding: 18px 20px; animation: pulse-r 2s infinite; }
.card-green { background: #001a0d; border: 1px solid var(--green);  border-radius: 12px; padding: 18px 20px; }
.card-amber { background: #130c00; border: 1px solid var(--amber);  border-radius: 12px; padding: 18px 20px; }
@keyframes pulse-r { 0%,100%{box-shadow:0 0 18px rgba(255,58,92,.25)} 50%{box-shadow:0 0 36px rgba(255,58,92,.55)} }

/* Section title */
.sec { font-family:'Orbitron',monospace; font-size:0.62rem; letter-spacing:.22em; color:var(--cyan);
       text-transform:uppercase; padding:4px 0 10px; border-bottom:1px solid var(--border); margin-bottom:1.1rem; }

/* Big numbers */
.big  { font-family:'Share Tech Mono',monospace; font-size:2.2rem; line-height:1.1; }
.med  { font-family:'Share Tech Mono',monospace; font-size:1.35rem; }
.sml  { font-family:'Share Tech Mono',monospace; font-size:0.88rem; }
.lbl  { font-size:0.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; margin-bottom:4px; }
.sub  { font-size:0.82rem; color:var(--muted); margin-top:4px; }

/* Progress */
.pbar-wrap { background:var(--bg); border:1px solid var(--dim); border-radius:6px; height:12px; overflow:hidden; margin:8px 0; }
.pbar-g { background:linear-gradient(90deg,var(--green),#00ffcc); height:100%; border-radius:6px; transition:width .4s; }
.pbar-a { background:linear-gradient(90deg,var(--amber),#ffdd44); height:100%; border-radius:6px; }
.pbar-r { background:linear-gradient(90deg,var(--red),#ff7799);   height:100%; border-radius:6px; }

/* Ticker */
.ticker-wrap { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:16px 18px; position:relative; overflow:hidden; }
.ticker-wrap::before { content:''; position:absolute; top:0;left:0;right:0; height:3px; background:linear-gradient(90deg,var(--cyan),transparent); }
.t-sym { font-family:'Orbitron',monospace; font-size:1rem; color:var(--cyan); }
.t-name { font-size:0.78rem; color:var(--muted); margin-top:2px; }
.t-price { font-family:'Share Tech Mono',monospace; font-size:1.9rem; margin:8px 0 4px; }
.t-badge-live { display:inline-block; background:var(--green); color:#000; font-family:'Share Tech Mono',monospace; font-size:0.58rem; padding:2px 7px; border-radius:3px; font-weight:bold; animation:blink 2s infinite; }
.t-badge-close { display:inline-block; background:var(--muted); color:#000; font-family:'Share Tech Mono',monospace; font-size:0.58rem; padding:2px 7px; border-radius:3px; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.4} }

::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:2px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA HELPERS
# ─────────────────────────────────────────────
def enc(obj): return base64.b64encode(json.dumps(obj, ensure_ascii=False).encode()).decode()
def dec(s, default):
    try: return json.loads(base64.b64decode(s).decode())
    except: return default

def qp(key, default, cast=str):
    try: return cast(st.query_params[key])
    except: return default

def save_all():
    st.query_params.update({
        "s1":  str(st.session_state.get("i_s1", 12000)),
        "s2":  str(st.session_state.get("i_s2", 7000)),
        "s3":  str(st.session_state.get("i_s3", 1081)),
        "pl":  str(st.session_state.get("i_pl", 1500000)),
        "pr":  str(st.session_state.get("i_pr", 2.4)),
        "pe":  str(st.session_state.get("i_pe", date.today() + timedelta(days=180))),
        "tn":  str(st.session_state.get("i_tn", 50000000)),
        "mi":  str(st.session_state.get("i_mi", 38000)),
        "wr":  str(st.session_state.get("i_wr", 4.0)),
        "dob": str(st.session_state.get("i_dob", date(1992, 12, 14))),
        "dca": enc(st.session_state.get("dca_records", [])),
    })

# ─────────────────────────────────────────────
# INIT SESSION STATE
# ─────────────────────────────────────────────
if "dca_records" not in st.session_state:
    st.session_state.dca_records = dec(qp("dca", "", str), [])

# ─────────────────────────────────────────────
# FETCH PRICE
# ─────────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch(ticker_tw):
    sym = ticker_tw + ".TW"
    r = {"price": None, "prev": None, "live": False, "err": None}
    try:
        t = yf.Ticker(sym)
        p = getattr(t.fast_info, "last_price", None)
        v = getattr(t.fast_info, "previous_close", None)
        if not p:
            h = t.history(period="5d")
            if h.empty: r["err"] = "N/A"; return r
            p = float(h["Close"].iloc[-1])
            v = float(h["Close"].iloc[-2]) if len(h) > 1 else p
        else:
            r["live"] = True
        r["price"] = float(p); r["prev"] = float(v) if v else float(p)
    except Exception as e:
        r["err"] = str(e)
    return r

def chg(p, v): return (p - v) / v * 100 if v else 0

def fmt(n, d=0): return f"${n:,.{d}f}"

def months_to_fire(net, target, monthly, mv_all, mv_008, mv_631, mv_233):
    w1 = mv_008/mv_all if mv_all else 1/3
    w2 = mv_631/mv_all if mv_all else 1/3
    w3 = mv_233/mv_all if mv_all else 1/3
    r  = (1 + (w1*.08 + w2*.14 + w3*.10)) ** (1/12) - 1
    m, cap = 0, 600
    while net < target and m < cap:
        net = net * (1 + r) + monthly
        m += 1
    return m

# ─────────────────────────────────────────────
# SIDEBAR — SETTINGS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ 設定")
    st.markdown("#### 持股數量")
    s_006208 = st.number_input("006208 股數", 0, value=qp("s1",12000,int),  step=100, key="i_s1")
    s_00631L = st.number_input("00631L 股數", 0, value=qp("s2",7000, int),  step=100, key="i_s2")
    s_2330   = st.number_input("2330 股數",   0, value=qp("s3",1081, int),  step=1,   key="i_s3")

    st.markdown("#### 質押條件")
    pledge_loan   = st.number_input("借款總額 (TWD)", 0, value=qp("pl",1500000,int), step=10000, key="i_pl")
    pledge_rate   = st.number_input("年利率 (%)", 0.0, value=qp("pr",2.4,float), step=0.1, format="%.2f", key="i_pr")
    pledge_expiry = st.date_input("到期日", value=qp("pe", date.today()+timedelta(days=180), date.fromisoformat), key="i_pe")

    st.markdown("#### 退休目標")
    target_net    = st.number_input("目標淨資產 (TWD)", 1000000, value=qp("tn",50000000,int), step=1000000, key="i_tn")
    monthly_inv   = st.number_input("每月定額投入 (TWD)", 0, value=qp("mi",38000,int), step=1000, key="i_mi")
    withdraw_rate = st.number_input("安全提領率 (%)", 1.0, 10.0, value=qp("wr",4.0,float), step=0.1, format="%.1f", key="i_wr")
    dob           = st.date_input("出生年月日", value=qp("dob",date(1992,12,14),date.fromisoformat), min_value=date(1950,1,1), key="i_dob")

    st.markdown("---")
    if st.button("💾 儲存設定", use_container_width=True): save_all(); st.success("✅ 已儲存")
    refresh = st.button("🔄 更新報價", use_container_width=True)

# ─────────────────────────────────────────────
# FETCH DATA
# ─────────────────────────────────────────────
if refresh: st.cache_data.clear()
d8 = fetch("006208"); d6 = fetch("00631L"); d3 = fetch("2330")

p8 = d8["price"] or 0; p6 = d6["price"] or 0; p3 = d3["price"] or 0
mv8 = p8 * s_006208; mv6 = p6 * s_00631L; mv3 = p3 * s_2330
total_mv  = mv8 + mv6 + mv3
net_asset = total_mv - pledge_loan
annual_int  = pledge_loan * pledge_rate / 100
monthly_int = annual_int / 12
days_left   = (pledge_expiry - date.today()).days
pledge_ratio = (mv8 / pledge_loan * 100) if pledge_loan > 0 else 9999
extra_borrow = (mv8 / 2.5) - pledge_loan
conv_pct     = min(mv6 / 1_000_000 * 100, 100)
conv_trigger = mv6 >= 1_000_000

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
now_str = datetime.now().strftime("%Y-%m-%d  %H:%M")
st.markdown(f"""
<div style='padding:4px 0 20px;'>
  <div style='font-family:Orbitron,monospace;font-size:1.6rem;color:var(--cyan);letter-spacing:.12em;
              text-shadow:0 0 24px rgba(0,212,255,.45);'>🔥 PROJECT F.I.R.E</div>
  <div style='font-family:Share Tech Mono,monospace;font-size:.7rem;color:var(--dim);
              letter-spacing:.15em;margin-top:3px;'>FINANCIAL INDEPENDENCE · RETIRE EARLY &nbsp;│&nbsp; {now_str}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECTION 1 — 即時報價
# ─────────────────────────────────────────────
st.markdown('<div class="sec">[ 01 ]  即時報價</div>', unsafe_allow_html=True)

def ticker_card(sym, name, d, shares, mv):
    p    = d["price"] or 0
    prev = d["prev"]  or p
    c    = chg(p, prev)
    ca   = p - prev
    clr  = "var(--green)" if c >= 0 else "var(--red)"
    icon = "▲" if c >= 0 else "▼"
    badge= f'<span class="t-badge-live">● LIVE</span>' if d["live"] and not d["err"] else f'<span class="t-badge-close">■ CLOSE</span>'
    err  = f'<span style="font-size:.7rem;color:var(--red);margin-left:6px;">⚠ {d["err"][:20]}</span>' if d["err"] else ""
    return f"""
    <div class="ticker-wrap">
      <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
        <div><div class="t-sym">{sym}</div><div class="t-name">{name}</div></div>
        <div>{badge}{err}</div>
      </div>
      <div class="t-price" style='color:var(--text);'>{p:,.2f} <span style='font-size:.9rem;color:var(--muted);'>TWD</span></div>
      <div style='font-family:Share Tech Mono,monospace;font-size:.88rem;color:{clr};'>{icon} {ca:+.2f} ({c:+.2f}%)</div>
      <div style='margin-top:10px;border-top:1px solid var(--border);padding-top:8px;'>
        <div class="sml" style='color:var(--green);'>{fmt(mv)}</div>
        <div style='font-size:.78rem;color:var(--muted);margin-top:2px;'>{shares:,} 股 × {p:,.2f}</div>
      </div>
    </div>"""

c1, c2, c3 = st.columns(3)
with c1: st.markdown(ticker_card("006208","富邦台50 ETF",       d8, s_006208, mv8), unsafe_allow_html=True)
with c2: st.markdown(ticker_card("00631L","富邦台灣50正2 ETF",  d6, s_00631L, mv6), unsafe_allow_html=True)
with c3: st.markdown(ticker_card("2330",  "台積電 TSMC",         d3, s_2330,   mv3), unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECTION 2 — 資產概覽
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="sec">[ 02 ]  資產概覽</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("總市值",  fmt(total_mv))
with c2: st.metric("質押借款", fmt(pledge_loan))
with c3: st.metric("總淨資產", fmt(net_asset), f"{net_asset/target_net*100:.1f}% of 目標")
with c4: st.metric("借款到期", f"{days_left} 天", "⚠ 注意" if days_left <= 60 else "安全")

c5, c6, c7, c8 = st.columns(4)
with c5: st.metric("年利率",    f"{pledge_rate:.2f}%")
with c6: st.metric("年利息",    fmt(annual_int))
with c7: st.metric("月利息",    fmt(monthly_int))
with c8: st.metric("到期日",    pledge_expiry.strftime("%Y/%m/%d"))

# ─────────────────────────────────────────────
# SECTION 3 — 核心訊號
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="sec">[ 03 ]  核心訊號</div>', unsafe_allow_html=True)

sig1, sig2, sig3 = st.columns(3)

# Signal 1 — 00631L 轉換進度
with sig1:
    if conv_trigger:
        cls = "card-red"; col = "var(--red)"; tag = "🚨 立即執行轉換！"
        bar = "pbar-r"
    elif conv_pct >= 70:
        cls = "card-amber"; col = "var(--amber)"; tag = "進行中 接近目標"
        bar = "pbar-a"
    else:
        cls = "card"; col = "var(--green)"; tag = "進行中"
        bar = "pbar-g"
    st.markdown(f"""
    <div class="{cls}">
      <div class="lbl">00631L → 100萬轉換進度</div>
      <div class="big" style='color:{col};'>{conv_pct:.1f}%</div>
      <div class="pbar-wrap"><div class="{bar}" style='width:{min(conv_pct,100):.1f}%;'></div></div>
      <div style='display:flex;justify-content:space-between;'>
        <span class="sml" style='color:var(--muted);'>{fmt(mv6)} / $1,000,000</span>
        <span class="sml" style='color:{col};'>{tag}</span>
      </div>
      <div style='font-size:.78rem;color:var(--muted);margin-top:6px;'>
        {'✅ 達標！賣出 00631L → 轉入 006208' if conv_trigger else f'尚差 {fmt(max(0,1000000-mv6))}'}
      </div>
    </div>""", unsafe_allow_html=True)

# Signal 2 — 質押維持率
with sig2:
    if pledge_loan == 0:
        cls="card-green"; col="var(--green)"; tag="無借款"; bar="pbar-g"
    elif pledge_ratio < 220:
        cls="card-red";   col="var(--red)";   tag="⚠ 危險！"; bar="pbar-r"
    elif pledge_ratio < 250:
        cls="card-amber"; col="var(--amber)"; tag="注意";  bar="pbar-a"
    else:
        cls="card-green"; col="var(--green)"; tag="安全";  bar="pbar-g"
    ratio_str = f"{pledge_ratio:.1f}" if pledge_loan > 0 else "∞"
    barpct = min(pledge_ratio/3.5, 100) if pledge_loan > 0 else 100
    st.markdown(f"""
    <div class="{cls}">
      <div class="lbl">006208 質押維持率</div>
      <div class="big" style='color:{col};'>{ratio_str}<span style='font-size:1.2rem;'>%</span></div>
      <div class="pbar-wrap"><div class="{bar}" style='width:{barpct:.1f}%;'></div></div>
      <div style='display:flex;justify-content:space-between;'>
        <span class="sml" style='color:var(--muted);'>警戒 220% ／ 安全 250%</span>
        <span class="sml" style='color:{col};'>{tag}</span>
      </div>
      <div style='font-size:.78rem;color:var(--muted);margin-top:6px;'>
        可增貸空間：<span style='color:{"var(--green)" if extra_borrow>=0 else "var(--red)"};'>{fmt(extra_borrow)}</span>
      </div>
    </div>""", unsafe_allow_html=True)

# Signal 3 — 退休達標率
with sig3:
    fire_pct = min(net_asset / target_net * 100, 100)
    col = "var(--green)" if fire_pct >= 100 else "var(--cyan)"
    st.markdown(f"""
    <div class="card">
      <div class="lbl">退休目標達成率（5,000萬）</div>
      <div class="big" style='color:{col};'>{fire_pct:.1f}%</div>
      <div class="pbar-wrap"><div class="pbar-g" style='width:{fire_pct:.1f}%;'></div></div>
      <div style='display:flex;justify-content:space-between;'>
        <span class="sml" style='color:var(--muted);'>{fmt(net_asset)}</span>
        <span class="sml" style='color:var(--muted);'>目標 {fmt(target_net)}</span>
      </div>
      <div style='font-size:.78rem;color:var(--muted);margin-top:6px;'>
        尚差 <span style='color:var(--amber);'>{fmt(max(0,target_net-net_asset))}</span>
      </div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECTION 4 — 退休預估
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="sec">[ 04 ]  退休預估</div>', unsafe_allow_html=True)

months = months_to_fire(net_asset, target_net, monthly_inv, total_mv, mv8, mv6, mv3)
retire_dt  = datetime.now() + timedelta(days=months * 30.44)
retire_str = retire_dt.strftime("%Y 年 %m 月")
age_days   = (retire_dt - datetime(dob.year, dob.month, dob.day)).days
retire_age = age_days / 365.25
monthly_passive = (target_net * withdraw_rate / 100) / 12
yrs = months // 12; mos = months % 12

# blended rate
w1 = mv8/total_mv if total_mv else 1/3
w2 = mv6/total_mv if total_mv else 1/3
w3 = mv3/total_mv if total_mv else 1/3
blended = (w1*.08 + w2*.14 + w3*.10) * 100

ra, rb = st.columns([3, 2])
with ra:
    st.markdown(f"""
    <div class="card" style='border-color:#1a3a5a;'>
      <div class="lbl">預估財務自由日</div>
      <div style='font-family:Orbitron,monospace;font-size:2rem;color:var(--cyan);margin:8px 0;'>{retire_str}</div>
      <div style='font-family:Orbitron,monospace;font-size:1.15rem;color:var(--green);margin-bottom:14px;'>屆時年齡：{retire_age:.1f} 歲</div>
      <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;'>
        <div>
          <div class="lbl">距今</div>
          <div class="med" style='color:var(--text);'>{months} 個月</div>
          <div class="sub">{yrs} 年 {mos} 個月</div>
        </div>
        <div>
          <div class="lbl">混合年化</div>
          <div class="med" style='color:var(--cyan);'>{blended:.2f}%</div>
          <div class="sub">加權估算</div>
        </div>
        <div>
          <div class="lbl">每月投入</div>
          <div class="med" style='color:var(--amber);'>{fmt(monthly_inv)}</div>
          <div class="sub">定期定額</div>
        </div>
      </div>
      <div style='font-size:.72rem;color:var(--dim);margin-top:12px;border-top:1px solid var(--border);padding-top:8px;'>
        假設：006208 年化 8% · 00631L 年化 14% · 2330 年化 10%
      </div>
    </div>""", unsafe_allow_html=True)

with rb:
    st.markdown(f"""
    <div style='display:flex;flex-direction:column;gap:12px;'>
      <div class="card-green">
        <div class="lbl">退休後每月被動收入</div>
        <div style='font-family:Orbitron,monospace;font-size:1.7rem;color:var(--green);
                    text-shadow:0 0 16px rgba(0,232,122,.4);margin:6px 0;'>{fmt(monthly_passive)}</div>
        <div class="sub">{fmt(target_net)} × {withdraw_rate:.1f}% ÷ 12</div>
        <div style='font-size:.72rem;color:var(--muted);margin-top:6px;'>✅ 4% 法則 · 免動用本金</div>
      </div>
      <div class="card">
        <div class="lbl">若提早退休（45歲）需要</div>
        <div class="med" style='color:var(--amber);'>{fmt(monthly_passive * 12 / 0.04 * 0.035)}</div>
        <div class="sub">以 3.5% 提領率計算</div>
      </div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECTION 5 — 定期定額追蹤
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="sec">[ 05 ]  00631L 定期定額追蹤</div>', unsafe_allow_html=True)

dca_c1, dca_c2 = st.columns([2, 3])
with dca_c1:
    st.markdown("##### 新增買入記錄")
    dca_date   = st.date_input("買入日期", value=date.today(), key="dca_d", label_visibility="collapsed")
    dca_shares = st.number_input("買入股數", min_value=1, value=1000, step=100, key="dca_s")
    dca_price  = st.number_input("買入價格", min_value=0.01,
                                  value=round(float(p6), 2) if p6 else 27.0,
                                  step=0.1, format="%.2f", key="dca_p")
    if st.button("➕  新增", use_container_width=True):
        st.session_state.dca_records.append({
            "date": str(dca_date), "shares": dca_shares,
            "price": round(dca_price, 2), "cost": round(dca_shares * dca_price)
        })
        st.session_state.dca_records.sort(key=lambda x: x["date"])
        save_all(); st.success("✅ 已新增")
    if st.session_state.dca_records:
        if st.button("🗑  刪除最後一筆", use_container_width=True):
            st.session_state.dca_records.pop(); save_all(); st.rerun()

with dca_c2:
    recs = st.session_state.dca_records
    if recs:
        tot_shares = sum(r["shares"] for r in recs)
        tot_cost   = sum(r["cost"]   for r in recs)
        avg_price  = tot_cost / tot_shares if tot_shares else 0
        cur_val    = tot_shares * p6
        pnl        = cur_val - tot_cost
        pnl_pct    = pnl / tot_cost * 100 if tot_cost else 0
        pnl_col    = "var(--green)" if pnl >= 0 else "var(--red)"
        target_gap = 1_000_000 - cur_val
        tpct       = min(cur_val / 1_000_000 * 100, 100)

        # Suggest monthly DCA: to reach 1M in ~18 months from current gap
        suggested_monthly = max(0, target_gap / 18) if target_gap > 0 else 0

        st.markdown(f"""
        <div class="card">
          <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px;'>
            <div>
              <div class="lbl">平均成本</div>
              <div class="med" style='color:var(--cyan);'>${avg_price:.2f}</div>
              <div class="sub">現價 ${p6:.2f}</div>
            </div>
            <div>
              <div class="lbl">未實現損益</div>
              <div class="med" style='color:{pnl_col};'>{fmt(pnl)}</div>
              <div class="sub" style='color:{pnl_col};'>{pnl_pct:+.2f}%</div>
            </div>
            <div>
              <div class="lbl">持股市值</div>
              <div class="med" style='color:var(--text);'>{fmt(cur_val)}</div>
              <div class="sub">{tot_shares:,} 股</div>
            </div>
          </div>
          <div class="lbl">100萬目標進度</div>
          <div class="pbar-wrap">
            <div class="{'pbar-g' if tpct>=100 else 'pbar-a'}" style='width:{tpct:.1f}%;'></div>
          </div>
          <div style='display:flex;justify-content:space-between;margin-bottom:10px;'>
            <span class="sml" style='color:var(--muted);'>{tpct:.1f}% 達成</span>
            <span class="sml" style='color:{"var(--green)" if target_gap<=0 else "var(--amber)"}'>
              {'🎯 達標！執行轉換' if target_gap<=0 else f'尚差 {fmt(max(0,target_gap))}'}
            </span>
          </div>
          <div style='background:#060d14;border:1px solid var(--border);border-radius:8px;padding:10px 14px;'>
            <div class="lbl">建議每月定額</div>
            <div class="med" style='color:var(--amber);'>{fmt(suggested_monthly)}</div>
            <div class="sub">以 18 個月內達成 100 萬估算</div>
          </div>
        </div>""", unsafe_allow_html=True)

        with st.expander(f"📋 買入記錄（共 {len(recs)} 筆）"):
            rows = ""
            for r in reversed(recs):
                rv   = r["shares"] * p6
                rpnl = rv - r["cost"]
                rc   = "var(--green)" if rpnl >= 0 else "var(--red)"
                rows += f"""<tr style='border-bottom:1px solid var(--border);'>
                  <td style='padding:8px 12px;font-family:Share Tech Mono,monospace;color:var(--cyan);font-size:.82rem;'>{r['date']}</td>
                  <td style='padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:.82rem;text-align:right;'>{r['shares']:,}</td>
                  <td style='padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:.82rem;text-align:right;'>${r['price']:.2f}</td>
                  <td style='padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:.82rem;text-align:right;'>{fmt(r['cost'])}</td>
                  <td style='padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:.82rem;text-align:right;color:{rc};'>{fmt(rpnl)}</td>
                </tr>"""
            st.markdown(f"""<div class="card" style='overflow-x:auto;padding:12px;'>
              <table style='width:100%;border-collapse:collapse;'>
                <thead><tr style='border-bottom:2px solid var(--border);'>
                  <th style='padding:8px 12px;font-size:.72rem;color:var(--muted);text-align:left;'>日期</th>
                  <th style='padding:8px 12px;font-size:.72rem;color:var(--muted);text-align:right;'>股數</th>
                  <th style='padding:8px 12px;font-size:.72rem;color:var(--muted);text-align:right;'>買價</th>
                  <th style='padding:8px 12px;font-size:.72rem;color:var(--muted);text-align:right;'>成本</th>
                  <th style='padding:8px 12px;font-size:.72rem;color:var(--muted);text-align:right;'>損益</th>
                </tr></thead>
                <tbody>{rows}</tbody>
              </table></div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="card" style="text-align:center;padding:32px;color:var(--muted);">尚無記錄，從左側新增第一筆買入</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECTION 6 — 收入配置
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="sec">[ 06 ]  收入配置計算機</div>', unsafe_allow_html=True)

tab_sal, tab_bonus = st.tabs(["💼  月薪配置", "🎁  獎金配置（5/1 績效 ＆ 1/1 年終）"])

# ── Tab 1: 月薪 ──
with tab_sal:
    sc1, sc2 = st.columns([2, 3])
    with sc1:
        net_sal   = st.number_input("月薪實領 (TWD)", 0, value=63000, step=1000, key="sal_net")
        dca_alloc = st.number_input("定期定額 00631L", 0, value=38000, step=1000, key="sal_dca")
        rent      = st.number_input("房租 / 房貸",     0, value=12000, step=500,  key="sal_rent")
        insurance = st.number_input("保險費",          0, value=2500,  step=100,  key="sal_ins")
        phone     = st.number_input("電信費",          0, value=999,   step=1,    key="sal_phone")
        sub       = st.number_input("訂閱 / 其他固定", 0, value=500,   step=100,  key="sal_sub")
        food      = st.number_input("飲食 / 日常生活", 0, value=8000,  step=500,  key="sal_food")
        fun       = st.number_input("娛樂 / 聚餐",     0, value=6000,  step=500,  key="sal_fun")

    with sc2:
        rigid  = rent + insurance + phone + sub
        living = food + fun
        total_out = dca_alloc + rigid + living + round(monthly_int)
        surplus   = net_sal - total_out
        s_col = "var(--green)" if surplus >= 0 else "var(--red)"
        s_pct = surplus / net_sal * 100 if net_sal else 0
        used_pct = min(total_out / net_sal * 100, 100) if net_sal else 0

        items = [
            ("📈 定期定額 00631L",  dca_alloc,        "var(--green)", "複利引擎"),
            ("🏠 剛性支出",         rigid,            "var(--red)",   f"房租{rent:,} 保險{insurance:,} 電信{phone:,} 訂閱{sub:,}"),
            ("🛒 生活費",           living,           "var(--cyan)",  f"飲食{food:,} 娛樂{fun:,}"),
            ("🏦 質押月息",         round(monthly_int),"#ff7799",     f"年利{pledge_rate:.2f}%"),
        ]
        rows = ""
        for name, amt, col, note in items:
            pct_item = amt / net_sal * 100 if net_sal else 0
            rows += f"""<tr style='border-bottom:1px solid var(--border);'>
              <td style='padding:9px 12px;font-size:.88rem;color:{col};'>{name}</td>
              <td style='padding:9px 12px;font-family:Share Tech Mono,monospace;font-size:.88rem;text-align:right;'>{fmt(amt)}</td>
              <td style='padding:9px 12px;font-family:Share Tech Mono,monospace;font-size:.8rem;color:var(--muted);text-align:right;'>{pct_item:.1f}%</td>
              <td style='padding:9px 12px;font-size:.75rem;color:var(--dim);'>{note}</td>
            </tr>"""

        advice = "💡 結餘建議加碼 00631L 或存定存" if surplus > 0 else f"⚠ 超支 {fmt(abs(surplus))}，建議縮減娛樂或生活費"

        st.markdown(f"""
        <div class="card">
          <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px;'>
            <div><div class="lbl">月薪實領</div><div class="med" style='color:var(--cyan);'>{fmt(net_sal)}</div></div>
            <div><div class="lbl">總支出</div><div class="med" style='color:var(--amber);'>{fmt(total_out)}</div><div class="sub">{used_pct:.1f}%</div></div>
            <div><div class="lbl">本月結餘</div><div class="med" style='color:{s_col};'>{fmt(surplus)}</div><div class="sub" style='color:{s_col};'>{s_pct:.1f}%</div></div>
          </div>
          <div class="pbar-wrap"><div class="{'pbar-g' if surplus>=0 else 'pbar-r'}" style='width:{used_pct:.1f}%;'></div></div>
          <table style='width:100%;border-collapse:collapse;margin-top:12px;'>
            <thead><tr style='border-bottom:2px solid var(--border);'>
              <th style='padding:9px 12px;font-size:.72rem;color:var(--muted);text-align:left;'>項目</th>
              <th style='padding:9px 12px;font-size:.72rem;color:var(--muted);text-align:right;'>金額</th>
              <th style='padding:9px 12px;font-size:.72rem;color:var(--muted);text-align:right;'>佔薪</th>
              <th style='padding:9px 12px;font-size:.72rem;color:var(--muted);text-align:left;'>說明</th>
            </tr></thead>
            <tbody>{rows}</tbody>
            <tfoot><tr style='border-top:2px solid var(--border);'>
              <td style='padding:10px 12px;font-size:.9rem;color:var(--cyan);font-weight:bold;'>本月結餘</td>
              <td style='padding:10px 12px;font-family:Share Tech Mono,monospace;font-size:1rem;color:{s_col};text-align:right;font-weight:bold;'>{fmt(surplus)}</td>
              <td style='padding:10px 12px;font-family:Share Tech Mono,monospace;font-size:.85rem;color:{s_col};text-align:right;'>{s_pct:.1f}%</td>
              <td style='padding:10px 12px;font-size:.78rem;color:{s_col};'>{advice}</td>
            </tfoot>
          </table>
        </div>""", unsafe_allow_html=True)

# ── Tab 2: 獎金 ──
with tab_bonus:
    bc1, bc2 = st.columns([2, 3])
    with bc1:
        bonus_type   = st.selectbox("獎金類型", ["🎁 績效獎金（5月1日）", "🎊 年終獎金（1月1日）"], key="b_type")
        bonus_gross  = st.number_input("獎金稅前金額", 0, value=113405, step=1000, key="b_gross")
        bonus_tax    = st.number_input("稅率 (%)", 0, 40, value=10, step=1, key="b_tax",
                                        help="補充保費 2.11% + 所得稅，建議填 10~15%")
        st.markdown("##### 配置方式")
        b_dca     = st.number_input("加碼 00631L",      0, value=90000, step=5000, key="b_dca")
        b_pledge  = st.number_input("提前還質押借款",   0, value=0,     step=10000,key="b_pledge",
                                     help=f"目前借款 {fmt(pledge_loan)}")
        b_save    = st.number_input("存定存 / 備用現金", 0, value=0,     step=5000, key="b_save")
        b_other   = st.number_input("其他用途",          0, value=0,     step=1000, key="b_other")

    with bc2:
        after_tax    = round(bonus_gross * (1 - bonus_tax / 100))
        total_alloc  = b_dca + b_pledge + b_save + b_other
        unalloc      = after_tax - total_alloc
        un_col       = "var(--green)" if unalloc >= 0 else "var(--red)"
        bar_p        = min(total_alloc / after_tax * 100, 100) if after_tax else 0
        int_saved    = b_pledge * pledge_rate / 100
        new_dca_val  = mv6 + b_dca
        new_dca_pct  = min(new_dca_val / 1_000_000 * 100, 100)

        # Months to 1M after bonus
        months_after = 0
        val = new_dca_val
        while val < 1_000_000 and months_after < 120:
            val += monthly_inv
            months_after += 1

        st.markdown(f"""
        <div class="card">
          <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px;'>
            <div><div class="lbl">稅後到手</div>
              <div class="med" style='color:var(--cyan);'>{fmt(after_tax)}</div>
              <div class="sub">扣除 {bonus_tax}% 稅</div></div>
            <div><div class="lbl">已配置</div>
              <div class="med" style='color:var(--amber);'>{fmt(total_alloc)}</div>
              <div class="sub">{bar_p:.1f}%</div></div>
            <div><div class="lbl">未配置</div>
              <div class="med" style='color:{un_col};'>{fmt(unalloc)}</div>
              <div class="sub">{'✅ 有結餘' if unalloc>=0 else '⚠ 超出'}</div></div>
          </div>
          <div class="pbar-wrap"><div class="{'pbar-g' if unalloc>=0 else 'pbar-r'}" style='width:{bar_p:.1f}%;'></div></div>
          <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px;'>
            <div style='background:#060d14;border:1px solid var(--border);border-radius:8px;padding:12px;'>
              <div class="lbl">加碼後 00631L 進度</div>
              <div class="med" style='color:var(--green);'>{new_dca_pct:.1f}%</div>
              <div class="pbar-wrap"><div class="pbar-g" style='width:{new_dca_pct:.1f}%;'></div></div>
              <div class="sub">{fmt(new_dca_val)} / $1,000,000</div>
              <div style='font-size:.75rem;color:var(--muted);margin-top:4px;'>
                加碼後約再 <span style='color:var(--amber);'>{months_after} 個月</span>達標
              </div>
            </div>
            <div style='background:#060d14;border:1px solid var(--border);border-radius:8px;padding:12px;'>
              <div class="lbl">還款後每年省息</div>
              <div class="med" style='color:var(--green);'>{fmt(int_saved)}</div>
              <div class="sub">還 {fmt(b_pledge)} × {pledge_rate:.2f}%</div>
              <div style='font-size:.75rem;color:var(--muted);margin-top:4px;'>
                等同年化 {pledge_rate:.2f}% 無風險報酬
              </div>
            </div>
          </div>
          <div style='margin-top:14px;padding-top:12px;border-top:1px solid var(--border);
                      font-size:.8rem;color:var(--muted);line-height:2;'>
            <span style='color:var(--cyan);font-family:Share Tech Mono,monospace;'>建議順序</span><br>
            <span style='color:var(--green);'>① 加碼 00631L</span> — 離 100 萬愈近愈好，達標後可轉換提升槓桿效益<br>
            <span style='color:var(--amber);'>② 評估還款</span> — 若質押維持率 &lt; 250%，優先補足擔保品<br>
            <span style='color:var(--muted);'>③ 定存備用</span> — 確定短期內會用到才存，其餘長期持有
          </div>
        </div>""", unsafe_allow_html=True)

        if unalloc > 0:
            st.markdown(f"""<div class="card-green" style='margin-top:8px;padding:12px 16px;'>
              <span style='font-size:.88rem;color:var(--green);'>
                💡 還有 {fmt(unalloc)} 未配置 — 建議全部加碼 00631L，加速達成 100 萬目標
              </span></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECTION 7 — 策略 SOP
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
with st.expander("📋  策略 SOP — F.I.R.E 操作守則"):
    st.markdown("""
    <div style='font-family:Share Tech Mono,monospace;font-size:.85rem;color:var(--muted);line-height:2.2;padding:4px 0;'>
      <span style='color:var(--cyan);'>PHASE 1</span> &nbsp;每月定期定額買入 <span style='color:var(--green);'>00631L</span>，累積至市值 ≥ 100萬<br>
      <span style='color:var(--cyan);'>PHASE 2</span> &nbsp;達標後全數賣出，轉入 <span style='color:var(--green);'>006208</span>，建立質押部位<br>
      <span style='color:var(--cyan);'>PHASE 3</span> &nbsp;維持 006208 質押率 ≥ 250%，借出資金持續買入 <span style='color:var(--green);'>2330</span><br>
      <span style='color:var(--amber);'>加碼時機</span> &nbsp;績效獎金（5/1）＆ 年終獎金（1/1）優先加碼 00631L<br>
      <span style='color:var(--red);'>風險控管</span> &nbsp;質押維持率 &lt; 220% 立即補充擔保品或還款
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style='text-align:center;padding:20px 0 8px;border-top:1px solid var(--border);margin-top:8px;'>
  <span style='font-family:Share Tech Mono,monospace;font-size:.65rem;color:var(--dim);letter-spacing:.12em;'>
    PROJECT F.I.R.E &nbsp;│&nbsp; NOT FINANCIAL ADVICE &nbsp;│&nbsp; DATA: YFINANCE &nbsp;│&nbsp; {now_str}
  </span>
</div>
""", unsafe_allow_html=True)
