import streamlit as st
import yfinance as yf
import pandas as pd
import json, base64, math
from datetime import datetime, date, timedelta

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Project F.I.R.E",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700&family=Noto+Sans+TC:wght@400;500;700&display=swap');
:root {
  --bg:#090d12; --card:#0f1923; --card2:#0a1520;
  --border:#1e3a4a; --border2:#0d2535;
  --cyan:#00d4ff; --green:#00e87a; --red:#ff3a5c;
  --amber:#ffb300; --purple:#b388ff; --pink:#ff6b9d;
  --text:#ddeef5; --muted:#6a9aaa; --dim:#2a4a5a;
}
html,body,[data-testid="stApp"]{background:var(--bg)!important;color:var(--text)!important;font-family:'Noto Sans TC',sans-serif;font-size:15px;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="block-container"]{padding:1rem 1.4rem 2rem!important;}

/* Sidebar */
[data-testid="stSidebar"]{background:#060a0f!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;font-size:0.95rem!important;}
[data-testid="stSidebar"] label{color:var(--muted)!important;font-size:0.78rem!important;text-transform:uppercase;letter-spacing:.05em;}
[data-testid="stSidebar"] input{background:var(--card)!important;border:1px solid var(--border)!important;color:var(--cyan)!important;font-size:1rem!important;min-height:44px!important;border-radius:6px!important;padding:8px 12px!important;}
[data-testid="stSidebar"] .stNumberInput input{font-size:1.05rem!important;font-family:'Share Tech Mono',monospace!important;}

/* Main inputs */
[data-testid="stNumberInput"] input,[data-testid="stTextInput"] input{
  background:var(--card)!important;border:1px solid var(--border)!important;
  color:var(--cyan)!important;font-size:1.05rem!important;min-height:44px!important;
  border-radius:6px!important;padding:8px 12px!important;font-family:'Share Tech Mono',monospace!important;}
[data-testid="stSelectbox"]>div>div{background:var(--card)!important;border:1px solid var(--border)!important;color:var(--cyan)!important;font-size:1rem!important;min-height:44px!important;}
[data-testid="stSlider"] .stSlider{padding:4px 0;}

/* Metrics */
[data-testid="stMetric"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:10px!important;padding:14px 16px!important;}
[data-testid="stMetricLabel"]{font-size:0.78rem!important;color:var(--muted)!important;text-transform:uppercase;letter-spacing:.06em;}
[data-testid="stMetricValue"]{font-family:'Share Tech Mono',monospace!important;font-size:1.45rem!important;color:var(--cyan)!important;}
[data-testid="stMetricDelta"]{font-size:0.82rem!important;}

/* Buttons */
.stButton button{background:var(--card)!important;border:1px solid var(--cyan)!important;color:var(--cyan)!important;font-size:0.92rem!important;min-height:44px!important;border-radius:8px!important;letter-spacing:.04em;transition:all .15s;}
.stButton button:hover{background:rgba(0,212,255,.08)!important;}
.btn-red button{border-color:var(--red)!important;color:var(--red)!important;}
.btn-green button{border-color:var(--green)!important;color:var(--green)!important;}
.btn-amber button{border-color:var(--amber)!important;color:var(--amber)!important;}

/* Tabs */
[data-testid="stTabs"] [role="tab"]{font-size:.88rem!important;color:var(--muted)!important;padding:8px 16px!important;}
[data-testid="stTabs"] [role="tab"][aria-selected="true"]{color:var(--cyan)!important;border-bottom:2px solid var(--cyan)!important;}
[data-testid="stTabPanel"]{padding-top:1rem!important;}

/* Expander */
[data-testid="stExpander"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:10px!important;}
details summary{font-size:.9rem!important;color:var(--cyan)!important;padding:4px 0!important;}

/* Cards */
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px 20px;}
.card-red{background:#140008;border:2px solid var(--red);border-radius:12px;padding:18px 20px;animation:pulse-r 2s infinite;}
.card-green{background:#001a0d;border:1px solid var(--green);border-radius:12px;padding:18px 20px;}
.card-amber{background:#130c00;border:1px solid var(--amber);border-radius:12px;padding:18px 20px;}
.card-purple{background:#0d0818;border:1px solid var(--purple);border-radius:12px;padding:18px 20px;}
@keyframes pulse-r{0%,100%{box-shadow:0 0 18px rgba(255,58,92,.25)}50%{box-shadow:0 0 40px rgba(255,58,92,.6)}}

/* Section title */
.sec{font-family:'Orbitron',monospace;font-size:.62rem;letter-spacing:.22em;color:var(--cyan);
     text-transform:uppercase;padding:4px 0 10px;border-bottom:1px solid var(--border);margin-bottom:1.1rem;}

/* Typography */
.big{font-family:'Share Tech Mono',monospace;font-size:2.2rem;line-height:1.1;}
.med{font-family:'Share Tech Mono',monospace;font-size:1.35rem;}
.sml{font-family:'Share Tech Mono',monospace;font-size:.88rem;}
.lbl{font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;}
.sub{font-size:.82rem;color:var(--muted);margin-top:4px;}
.mono{font-family:'Share Tech Mono',monospace;}

/* Progress */
.pbar-wrap{background:var(--bg);border:1px solid var(--dim);border-radius:6px;height:12px;overflow:hidden;margin:8px 0;}
.pbar-g{background:linear-gradient(90deg,var(--green),#00ffcc);height:100%;border-radius:6px;transition:width .4s;}
.pbar-a{background:linear-gradient(90deg,var(--amber),#ffdd44);height:100%;border-radius:6px;}
.pbar-r{background:linear-gradient(90deg,var(--red),#ff7799);height:100%;border-radius:6px;}
.pbar-p{background:linear-gradient(90deg,var(--purple),#e040fb);height:100%;border-radius:6px;}
.pbar-c{background:linear-gradient(90deg,var(--cyan),#00aaff);height:100%;border-radius:6px;}

/* Ticker */
.ticker-wrap{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 18px;position:relative;overflow:hidden;}
.ticker-wrap::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--cyan),transparent);}
.t-sym{font-family:'Orbitron',monospace;font-size:1rem;color:var(--cyan);}
.t-name{font-size:.78rem;color:var(--muted);margin-top:2px;}
.t-price{font-family:'Share Tech Mono',monospace;font-size:1.9rem;margin:8px 0 4px;}
.badge-live{display:inline-block;background:var(--green);color:#000;font-family:'Share Tech Mono',monospace;font-size:.58rem;padding:2px 7px;border-radius:3px;font-weight:bold;animation:blink 2s infinite;}
.badge-close{display:inline-block;background:var(--muted);color:#000;font-family:'Share Tech Mono',monospace;font-size:.58rem;padding:2px 7px;border-radius:3px;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.4}}

/* Panic mode */
.panic-blur{filter:blur(8px);user-select:none;pointer-events:none;}

::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def enc(obj): return base64.b64encode(json.dumps(obj, ensure_ascii=False).encode()).decode()
def dec(s, default):
    try: return json.loads(base64.b64decode(s).decode())
    except: return default
def qp(key, default, cast=str):
    try: return cast(st.query_params[key])
    except: return default
def fmt(n, d=0): return f"${n:,.{d}f}"
def fmtm(n): return f"{n/10000:.1f}萬"

def monthly_payment(principal, annual_rate, months):
    if annual_rate == 0: return principal / months
    r = annual_rate / 100 / 12
    return principal * r * (1+r)**months / ((1+r)**months - 1)

@st.cache_data(ttl=90)
def fetch(ticker_tw):
    sym = ticker_tw + ".TW"
    r = {"price": None, "prev": None, "live": False, "err": None}
    try:
        t = yf.Ticker(sym)
        p = getattr(t.fast_info, "last_price", None)
        v = getattr(t.fast_info, "previous_close", None)
        if p and float(p) > 0:
            r["price"] = float(p); r["prev"] = float(v) if v and float(v) > 0 else float(p)
            r["live"] = True; return r
    except: pass
    try:
        h = yf.Ticker(sym).history(period="5d", auto_adjust=True)
        if not h.empty:
            r["price"] = float(h["Close"].iloc[-1])
            r["prev"]  = float(h["Close"].iloc[-2]) if len(h)>1 else r["price"]
            return r
    except: pass
    try:
        h = yf.download(sym, period="5d", progress=False, auto_adjust=True)
        if not h.empty:
            r["price"] = float(h["Close"].iloc[-1])
            r["prev"]  = float(h["Close"].iloc[-2]) if len(h)>1 else r["price"]
            return r
    except Exception as e: r["err"] = str(e)[:30]
    return r

def months_to_fire(net, target, monthly, mv_all, mv8, mv6, mv3):
    if mv_all <= 0: w1=w2=w3=1/3
    else: w1=mv8/mv_all; w2=mv6/mv_all; w3=mv3/mv_all
    rate = (1+(w1*.08+w2*.14+w3*.10))**(1/12)-1
    m = 0
    while net < target and m < 600:
        net = net*(1+rate)+monthly; m+=1
    return m

def months_to_fire_rate(net, target, monthly, annual_rate):
    r = (1+annual_rate/100)**(1/12)-1
    m = 0
    while net < target and m < 600:
        net = net*(1+r)+monthly; m+=1
    return m

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "dca_records" not in st.session_state:
    st.session_state.dca_records = dec(qp("dca","",str), [])
if "panic_mode" not in st.session_state:
    st.session_state.panic_mode = False

def save_all():
    st.query_params.update({
        "s1": str(st.session_state.get("i_s1",12000)),
        "s2": str(st.session_state.get("i_s2",7000)),
        "s3": str(st.session_state.get("i_s3",1081)),
        "pl": str(st.session_state.get("i_pl",1500000)),
        "pr": str(st.session_state.get("i_pr",2.4)),
        "pe": str(st.session_state.get("i_pe", date.today()+timedelta(days=180))),
        "tn": str(st.session_state.get("i_tn",50000000)),
        "mi": str(st.session_state.get("i_mi",38000)),
        "wr": str(st.session_state.get("i_wr",4.0)),
        "dob": str(st.session_state.get("i_dob",date(1992,12,14))),
        "dca": enc(st.session_state.get("dca_records",[])),
    })

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ 持股與目標設定")

    st.markdown("#### 📊 持股數量")
    s_006208 = st.number_input("006208 股數", min_value=0, value=qp("s1",12000,int), step=100, key="i_s1")
    s_00631L = st.number_input("00631L 股數", min_value=0, value=qp("s2",7000, int), step=100, key="i_s2")
    s_2330   = st.number_input("2330 股數",   min_value=0, value=qp("s3",1081, int), step=1,   key="i_s3")

    st.markdown("#### 🏦 質押條件")
    pledge_loan   = st.number_input("質押借款 (TWD)", min_value=0, value=qp("pl",1500000,int), step=10000, key="i_pl")
    pledge_rate   = st.number_input("質押年利率 (%)", min_value=0.0, value=qp("pr",2.4,float), step=0.1, format="%.2f", key="i_pr")
    pledge_expiry = st.date_input("到期日", value=qp("pe", date.today()+timedelta(days=180), date.fromisoformat), key="i_pe")

    st.markdown("#### 🎯 退休目標")
    target_net  = st.number_input("目標淨資產 (TWD)", min_value=1000000, value=qp("tn",50000000,int), step=1000000, key="i_tn")
    monthly_inv = st.number_input("每月定額投入 (TWD)", min_value=0, value=qp("mi",38000,int), step=1000, key="i_mi")
    withdraw_rt = st.number_input("安全提領率 (%)", 1.0, 10.0, value=qp("wr",4.0,float), step=0.1, format="%.1f", key="i_wr")
    dob         = st.date_input("出生年月日", value=qp("dob",date(1992,12,14),date.fromisoformat), min_value=date(1950,1,1), key="i_dob")

    st.markdown("---")
    if st.button("💾 儲存設定", use_container_width=True): save_all(); st.success("✅ 已儲存！")
    if st.button("🔄 更新報價", use_container_width=True): st.cache_data.clear(); st.rerun()

    st.markdown("---")
    # PANIC BUTTON
    panic_label = "🔓 顯示金額" if st.session_state.panic_mode else "🚨 隱藏金額 (Panic)"
    if st.button(panic_label, use_container_width=True):
        st.session_state.panic_mode = not st.session_state.panic_mode
        st.rerun()
    if st.session_state.panic_mode:
        st.markdown('<div style="font-size:.75rem;color:var(--red);text-align:center;">⚠ 金額隱藏中，僅顯示達成率</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FETCH DATA
# ─────────────────────────────────────────────
d8 = fetch("006208"); d6 = fetch("00631L"); d3 = fetch("2330")
p8 = d8["price"] or 0; p6 = d6["price"] or 0; p3 = d3["price"] or 0
mv8 = p8*s_006208; mv6 = p6*s_00631L; mv3 = p3*s_2330
total_mv  = mv8+mv6+mv3
net_asset = total_mv - pledge_loan
monthly_int = pledge_loan*pledge_rate/100/12
pledge_ratio = (mv8/pledge_loan*100) if pledge_loan>0 else 9999
conv_pct  = min(mv6/1_000_000*100, 100)
panic     = st.session_state.panic_mode

def show_val(val, fmt_fn=fmt):
    return "█████" if panic else fmt_fn(val)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
now_str = datetime.now().strftime("%Y-%m-%d  %H:%M")
hcol1, hcol2 = st.columns([4,1])
with hcol1:
    st.markdown(f"""
    <div style='padding:2px 0 18px;'>
      <div style='font-family:Orbitron,monospace;font-size:1.6rem;color:var(--cyan);letter-spacing:.12em;
                  text-shadow:0 0 24px rgba(0,212,255,.4);'>🔥 PROJECT F.I.R.E</div>
      <div style='font-family:Share Tech Mono,monospace;font-size:.68rem;color:var(--dim);
                  letter-spacing:.15em;margin-top:3px;'>FINANCIAL INDEPENDENCE · RETIRE EARLY &nbsp;│&nbsp; {now_str}</div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tabs = st.tabs([
    "📈 資產總覽",
    "🏦 信貸模擬",
    "⚡ 壓力測試",
    "🎯 退休預估",
    "📋 定期定額",
    "💼 收入配置",
])

# ════════════════════════════════════════════
# TAB 1 — 資產總覽
# ════════════════════════════════════════════
with tabs[0]:
    # Ticker Cards
    st.markdown('<div class="sec">[ 01 ]  即時報價</div>', unsafe_allow_html=True)

    def chg(p, v): return (p-v)/v*100 if v else 0

    def ticker_card(sym, name, d, shares, mv):
        p=d["price"] or 0; prev=d["prev"] or p
        c=chg(p,prev); ca=p-prev
        clr="var(--green)" if c>=0 else "var(--red)"
        icon="▲" if c>=0 else "▼"
        badge=f'<span class="badge-live">● LIVE</span>' if d["live"] and not d["err"] else f'<span class="badge-close">■ CLOSE</span>'
        err=f'<span style="font-size:.68rem;color:var(--red);"> ⚠ {d["err"][:18]}</span>' if d["err"] else ""
        mv_str = "█████" if panic else fmt(mv)
        return f"""
        <div class="ticker-wrap">
          <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px;'>
            <div><div class="t-sym">{sym}</div><div class="t-name">{name}</div></div>
            <div>{badge}{err}</div>
          </div>
          <div class="t-price">{p:,.2f} <span style='font-size:.88rem;color:var(--muted);'>TWD</span></div>
          <div style='font-family:Share Tech Mono,monospace;font-size:.88rem;color:{clr};'>{icon} {ca:+.2f} ({c:+.2f}%)</div>
          <div style='margin-top:10px;border-top:1px solid var(--border);padding-top:8px;'>
            <div class="sml" style='color:var(--green);'>{mv_str}</div>
            <div style='font-size:.78rem;color:var(--muted);margin-top:2px;'>{shares:,} 股 × {p:,.2f}</div>
          </div>
        </div>"""

    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(ticker_card("006208","富邦台50 ETF",      d8,s_006208,mv8), unsafe_allow_html=True)
    with c2: st.markdown(ticker_card("00631L","富邦台灣50正2 ETF", d6,s_00631L,mv6), unsafe_allow_html=True)
    with c3: st.markdown(ticker_card("2330",  "台積電 TSMC",        d3,s_2330,  mv3), unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="sec">[ 02 ]  資產概覽</div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("總市值",  show_val(total_mv))
    with c2: st.metric("質押借款", show_val(pledge_loan))
    with c3: st.metric("總淨資產", show_val(net_asset), f"{net_asset/target_net*100:.1f}% of 目標")
    with c4:
        days_left = (pledge_expiry-date.today()).days
        st.metric("借款到期", f"{days_left} 天", "⚠ 注意" if days_left<=60 else "安全")

    c5,c6,c7,c8 = st.columns(4)
    with c5: st.metric("年利率", f"{pledge_rate:.2f}%")
    with c6: st.metric("年利息", show_val(pledge_loan*pledge_rate/100))
    with c7: st.metric("月利息", show_val(monthly_int))
    with c8: st.metric("到期日", pledge_expiry.strftime("%Y/%m/%d"))

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="sec">[ 03 ]  核心訊號</div>', unsafe_allow_html=True)

    sig1,sig2,sig3 = st.columns(3)

    with sig1:
        if mv6>=1_000_000: cls="card-red"; col="var(--red)"; tag="🚨 立即執行轉換！"; bar="pbar-r"
        elif conv_pct>=70: cls="card-amber"; col="var(--amber)"; tag="接近目標"; bar="pbar-a"
        else: cls="card"; col="var(--green)"; tag="進行中"; bar="pbar-g"
        gap_str = "達標！賣出轉入 006208" if mv6>=1_000_000 else f"尚差 {show_val(max(0,1000000-mv6))}"
        st.markdown(f"""<div class="{cls}">
          <div class="lbl">00631L → 100萬轉換進度</div>
          <div class="big" style='color:{col};'>{conv_pct:.1f}%</div>
          <div class="pbar-wrap"><div class="{bar}" style='width:{conv_pct:.1f}%;'></div></div>
          <div style='display:flex;justify-content:space-between;'>
            <span class="sml" style='color:var(--muted);'>{show_val(mv6)} / $1,000,000</span>
            <span class="sml" style='color:{col};'>{tag}</span>
          </div>
          <div style='font-size:.78rem;color:var(--muted);margin-top:6px;'>{gap_str}</div>
        </div>""", unsafe_allow_html=True)

    with sig2:
        if pledge_loan==0: cls="card-green"; col="var(--green)"; tag="無借款"; barpct=100; bar="pbar-g"
        elif pledge_ratio<220: cls="card-red"; col="var(--red)"; tag="⚠ 危險！"; barpct=min(pledge_ratio/3.5,100); bar="pbar-r"
        elif pledge_ratio<250: cls="card-amber"; col="var(--amber)"; tag="注意"; barpct=min(pledge_ratio/3.5,100); bar="pbar-a"
        else: cls="card-green"; col="var(--green)"; tag="安全"; barpct=min(pledge_ratio/3.5,100); bar="pbar-g"
        ratio_str=f"{pledge_ratio:.1f}" if pledge_loan>0 else "∞"
        extra=(mv8/2.5)-pledge_loan if pledge_loan>0 else 0
        st.markdown(f"""<div class="{cls}">
          <div class="lbl">006208 質押維持率</div>
          <div class="big" style='color:{col};'>{ratio_str}<span style='font-size:1.2rem;'>%</span></div>
          <div class="pbar-wrap"><div class="{bar}" style='width:{barpct:.1f}%;'></div></div>
          <div style='display:flex;justify-content:space-between;'>
            <span class="sml" style='color:var(--muted);'>警戒220% / 安全250%</span>
            <span class="sml" style='color:{col};'>{tag}</span>
          </div>
          <div style='font-size:.78rem;color:var(--muted);margin-top:6px;'>
            可增貸：<span style='color:{"var(--green)" if extra>=0 else "var(--red)"};'>{show_val(extra)}</span>
          </div>
        </div>""", unsafe_allow_html=True)

    with sig3:
        fire_pct=min(net_asset/target_net*100,100) if target_net>0 else 0
        col="var(--green)" if fire_pct>=100 else "var(--cyan)"
        months=months_to_fire(net_asset,target_net,monthly_inv,total_mv,mv8,mv6,mv3)
        retire_dt=datetime.now()+timedelta(days=months*30.44)
        retire_str=retire_dt.strftime("%Y年%m月")
        st.markdown(f"""<div class="card">
          <div class="lbl">退休目標達成率（{fmtm(target_net)}）</div>
          <div class="big" style='color:{col};'>{fire_pct:.1f}%</div>
          <div class="pbar-wrap"><div class="pbar-c" style='width:{fire_pct:.1f}%;'></div></div>
          <div style='display:flex;justify-content:space-between;'>
            <span class="sml" style='color:var(--muted);'>{show_val(net_asset)}</span>
            <span class="sml" style='color:var(--muted);'>目標 {fmtm(target_net)}</span>
          </div>
          <div style='font-size:.78rem;color:var(--amber);margin-top:6px;'>預估 {retire_str} 達標</div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 2 — 信貸模擬
# ════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="sec">[ 04 ]  信貸模擬器 · LOAN SIMULATOR</div>', unsafe_allow_html=True)

    lc1, lc2 = st.columns([2,3])
    with lc1:
        st.markdown("#### 📝 信貸參數")
        loan_p    = st.number_input("總借款金額", min_value=0, value=1500000, step=50000, key="ln_p")
        loan_r    = st.number_input("年利率 (%)", min_value=0.0, value=2.12, step=0.01, format="%.2f", key="ln_r")
        loan_m    = st.number_input("還款期數 (月)", min_value=1, value=120, step=12, key="ln_m")
        loan_buf  = st.number_input("還款緩衝金 (預留不投入)", min_value=0, value=500000, step=50000, key="ln_buf")
        invest_target = st.selectbox("投入標的", ["00631L（正2，高波動高報酬）","006208（穩健，低波動）","2330（台積電）"], key="ln_target")

        st.markdown("#### 💼 現金流監控")
        net_sal  = st.number_input("實領月薪", min_value=0, value=63000, step=1000, key="cf_sal")
        rec_inv  = st.number_input("每月定期定額", min_value=0, value=38000, step=1000, key="cf_inv")
        pl_int   = st.number_input("質押利息支出/月", min_value=0, value=round(int(monthly_int)), step=100, key="cf_pl")
        life_min = st.number_input("最低生活費底線", min_value=0, value=15000, step=1000, key="cf_min")

    with lc2:
        monthly_rep = monthly_payment(loan_p, loan_r, loan_m)
        investable  = loan_p - loan_buf
        buf_months  = loan_buf / monthly_rep if monthly_rep > 0 else 0

        available_cash = net_sal - rec_inv - pl_int - monthly_rep
        cash_ok = available_cash >= life_min
        cash_col  = "var(--green)" if cash_ok else "var(--red)"
        cash_cls  = "card-green" if cash_ok else "card-red"
        cash_msg  = "✅ 現金流健康" if cash_ok else f"⚠ 缺口 {fmt(life_min - available_cash)}，建議減少定額或降低借款"

        # KPI row
        k1,k2,k3 = st.columns(3)
        with k1:
            st.markdown(f"""<div class="card" style='text-align:center;'>
              <div class="lbl">月還款額</div>
              <div class="med" style='color:var(--red);'>{fmt(monthly_rep)}</div>
              <div class="sub">本息平均攤還</div>
            </div>""", unsafe_allow_html=True)
        with k2:
            st.markdown(f"""<div class="card" style='text-align:center;'>
              <div class="lbl">可投入股市</div>
              <div class="med" style='color:var(--green);'>{fmt(investable)}</div>
              <div class="sub">扣除緩衝 {fmtm(loan_buf)}</div>
            </div>""", unsafe_allow_html=True)
        with k3:
            st.markdown(f"""<div class="card" style='text-align:center;'>
              <div class="lbl">緩衝金可撐</div>
              <div class="med" style='color:var(--amber);'>{buf_months:.1f} 個月</div>
              <div class="sub">不靠薪水還款</div>
            </div>""", unsafe_allow_html=True)

        # Cash flow monitor
        st.markdown(f"""<div class="{cash_cls}" style='margin-top:12px;'>
          <div class="lbl">💰 可用生活費監控</div>
          <div style='display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:12px;margin:10px 0;'>
            <div><div class="lbl">月薪</div><div class="sml" style='color:var(--cyan);'>{fmt(net_sal)}</div></div>
            <div><div class="lbl">定期定額</div><div class="sml" style='color:var(--amber);'>- {fmt(rec_inv)}</div></div>
            <div><div class="lbl">質押利息</div><div class="sml" style='color:var(--amber);'>- {fmt(pl_int)}</div></div>
            <div><div class="lbl">信貸月還款</div><div class="sml" style='color:var(--red);'>- {fmt(monthly_rep)}</div></div>
          </div>
          <div style='border-top:1px solid rgba(255,255,255,.1);padding-top:10px;display:flex;justify-content:space-between;align-items:center;'>
            <div>
              <div class="lbl">可用生活費</div>
              <div class="med" style='color:{cash_col};'>{fmt(available_cash)}</div>
            </div>
            <div>
              <div class="lbl">最低底線</div>
              <div class="med" style='color:var(--muted);'>{fmt(life_min)}</div>
            </div>
            <div style='font-size:.9rem;color:{cash_col};font-weight:bold;'>{cash_msg}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Loan summary
        total_int = monthly_rep * loan_m - loan_p
        st.markdown(f"""<div class="card" style='margin-top:12px;'>
          <div class="lbl">📊 借款總覽</div>
          <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:10px;'>
            <div><div class="lbl">總利息支出</div><div class="sml" style='color:var(--red);'>{fmt(total_int)}</div></div>
            <div><div class="lbl">總還款金額</div><div class="sml" style='color:var(--amber);'>{fmt(monthly_rep*loan_m)}</div></div>
            <div><div class="lbl">有效年利成本</div><div class="sml" style='color:var(--muted);'>{loan_r:.2f}%</div></div>
          </div>
          <div style='font-size:.75rem;color:var(--dim);margin-top:10px;'>
            若投入 {fmtm(investable)} 於 00631L（年化14%估算），10年後預估市值：
            <span style='color:var(--green);font-family:Share Tech Mono,monospace;'>
              {fmt(investable * (1.14**10))}
            </span>
            &nbsp;vs 總利息 {fmt(total_int)}
          </div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 3 — 壓力測試
# ════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="sec">[ 05 ]  2008 極限壓力測試 · DISASTER RECOVERY</div>', unsafe_allow_html=True)

    st.markdown("""<div class="card-amber" style='margin-bottom:16px;'>
      <div style='font-size:.88rem;color:var(--amber);'>
        ⚡ 模擬大盤崩跌 20% / 40% / 60%，評估你的質押部位是否安全、信貸緩衝金能撐多久
      </div>
    </div>""", unsafe_allow_html=True)

    sc1, sc2 = st.columns([1,2])
    with sc1:
        st.markdown("#### 🛡 壓測參數")
        emergency_fund = st.number_input("緊急預備金 (TWD)", min_value=0, value=400000, step=10000, key="st_em")
        credit_remain  = st.number_input("剩餘信貸子彈", min_value=0, value=500000, step=10000, key="st_cr",
                                          help="信貸中預留未投入股市的緩衝金")
        mt_repayment   = st.number_input("每月還款額", min_value=0, value=int(monthly_payment(1500000,2.12,120)), step=100, key="st_rep")
        unemployed_living = st.number_input("失業時月生活費", min_value=0, value=20000, step=1000, key="st_life")
        forced_call_ratio = st.number_input("斷頭維持率 (%)", min_value=100, value=130, step=5, key="st_fc",
                                              help="維持率低於此值券商強制平倉")

    with sc2:
        scenarios = [("跌20%", 0.20), ("跌40%", 0.40), ("跌60%", 0.60)]

        for label, drop in scenarios:
            new_mv8       = mv8 * (1 - drop)
            new_ratio     = (new_mv8 / pledge_loan * 100) if pledge_loan > 0 else 9999
            is_forced     = new_ratio < forced_call_ratio
            ratio_gap     = forced_call_ratio - new_ratio

            # How much cash needed to restore ratio to 130%
            if is_forced and pledge_loan > 0:
                needed_mv8     = pledge_loan * forced_call_ratio / 100
                mv8_gap        = needed_mv8 - new_mv8
                cash_can_help  = (emergency_fund + credit_remain) / (p8*(1-drop)) if p8*(1-drop)>0 else 0
                after_rescue_ratio = ((new_mv8 + (emergency_fund+credit_remain)) / pledge_loan * 100) if pledge_loan>0 else 9999
            else:
                mv8_gap = 0; cash_can_help = 0
                after_rescue_ratio = new_ratio

            # Survival months
            total_reserve   = emergency_fund + credit_remain
            monthly_burn    = unemployed_living + mt_repayment
            survive_months  = total_reserve / monthly_burn if monthly_burn > 0 else 999

            cls  = "card-red" if is_forced else ("card-amber" if new_ratio < 200 else "card-green")
            col  = "var(--red)" if is_forced else ("var(--amber)" if new_ratio < 200 else "var(--green)")
            icon = "💀" if is_forced else ("⚠️" if new_ratio < 200 else "✅")

            st.markdown(f"""<div class="{cls}" style='margin-bottom:12px;'>
              <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>
                <div style='font-family:Orbitron,monospace;font-size:1rem;color:{col};'>{icon} 大盤{label}</div>
                <div style='font-family:Share Tech Mono,monospace;font-size:.88rem;color:var(--muted);'>
                  006208: {fmt(new_mv8)} &nbsp;|&nbsp; 原市值 {fmt(mv8)}
                </div>
              </div>
              <div style='display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;'>
                <div>
                  <div class="lbl">質押維持率</div>
                  <div class="med" style='color:{col};'>{new_ratio:.1f}%</div>
                  <div class="sub">{'🔴 觸發斷頭' if is_forced else '✅ 安全'}</div>
                </div>
                <div>
                  <div class="lbl">救災後維持率</div>
                  <div class="med" style='color:var(--cyan);'>{after_rescue_ratio:.1f}%</div>
                  <div class="sub">動用全部預備金</div>
                </div>
                <div>
                  <div class="lbl">失業生存月數</div>
                  <div class="med" style='color:var(--amber);'>{survive_months:.1f} 月</div>
                  <div class="sub">月燒 {fmt(monthly_burn)}</div>
                </div>
                <div>
                  <div class="lbl">缺口金額</div>
                  <div class="med" style='color:{"var(--red)" if mv8_gap>0 else "var(--green)"};'>
                    {fmt(mv8_gap) if mv8_gap>0 else "無缺口"}
                  </div>
                  <div class="sub">{'需補充擔保品' if mv8_gap>0 else '儲備充足'}</div>
                </div>
              </div>
              {f'<div style="font-size:.78rem;color:var(--red);margin-top:8px;border-top:1px solid rgba(255,58,92,.3);padding-top:8px;">🚨 觸發強制平倉！緊急備用金＋信貸子彈共 {fmt(emergency_fund+credit_remain)}，動用後維持率提升至 {after_rescue_ratio:.1f}%</div>' if is_forced else ""}
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="card" style='margin-top:4px;'>
          <div style='font-size:.8rem;color:var(--muted);line-height:2;'>
            <span style='color:var(--cyan);font-family:Share Tech Mono,monospace;'>壓測結論</span><br>
            緊急預備金 {fmt(emergency_fund)} ＋ 信貸子彈 {fmt(credit_remain)} = 總救災力 {fmt(emergency_fund+credit_remain)}<br>
            失業情境：每月消耗 {fmt(monthly_burn)}，可支撐 <span style='color:var(--amber);'>{survive_months:.1f} 個月</span><br>
            建議：維持率務必保持 ≥ 250%，跌至 220% 即啟動補倉或還款
          </div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 4 — 退休預估
# ════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="sec">[ 06 ]  退休預估 · RETIREMENT PROJECTION</div>', unsafe_allow_html=True)

    rc1, rc2 = st.columns([2,3])
    with rc1:
        ret_rate = st.slider("📈 預設年化報酬率 (%)", 5, 20, 15,
                             help="含正2槓桿效益，保守估 10%，樂觀估 15-20%")
        extra_monthly = st.number_input("若加信貸，每月多投入", min_value=0, value=0, step=1000, key="ret_extra")
        loan_investable_ret = st.number_input("信貸一次性投入", min_value=0, value=0, step=50000, key="ret_loan")

    with rc2:
        # No loan scenario
        m_base = months_to_fire_rate(net_asset, target_net, monthly_inv, ret_rate)
        # With loan scenario
        net_with_loan = net_asset + loan_investable_ret
        m_loan = months_to_fire_rate(net_with_loan, target_net, monthly_inv + extra_monthly, ret_rate)
        diff_months = m_base - m_loan

        def calc_retire(months):
            dt = datetime.now() + timedelta(days=months*30.44)
            age = (dt - datetime(dob.year,dob.month,dob.day)).days/365.25
            return dt.strftime("%Y年%m月"), age

        base_date, base_age   = calc_retire(m_base)
        loan_date, loan_age   = calc_retire(m_loan)
        monthly_passive = (target_net * withdraw_rt / 100) / 12

        st.markdown(f"""<div class="card" style='margin-bottom:12px;'>
          <div style='display:grid;grid-template-columns:1fr 1fr;gap:20px;'>
            <div style='border-right:1px solid var(--border);padding-right:20px;'>
              <div class="lbl" style='color:var(--muted);'>🚫 不借款方案</div>
              <div style='font-family:Orbitron,monospace;font-size:1.6rem;color:var(--cyan);margin:8px 0;'>{base_date}</div>
              <div style='font-family:Orbitron,monospace;font-size:1rem;color:var(--muted);'>年齡 {base_age:.1f} 歲</div>
              <div class="sub" style='margin-top:8px;'>{m_base} 個月（{m_base//12}年{m_base%12}月）</div>
            </div>
            <div>
              <div class="lbl" style='color:var(--green);'>✅ 加槓桿方案</div>
              <div style='font-family:Orbitron,monospace;font-size:1.6rem;color:var(--green);margin:8px 0;'>{loan_date}</div>
              <div style='font-family:Orbitron,monospace;font-size:1rem;color:var(--green);'>年齡 {loan_age:.1f} 歲</div>
              <div class="sub" style='margin-top:8px;'>{m_loan} 個月（{m_loan//12}年{m_loan%12}月）</div>
            </div>
          </div>
          <div style='margin-top:14px;padding-top:12px;border-top:1px solid var(--border);text-align:center;'>
            <span style='font-family:Orbitron,monospace;font-size:1.1rem;color:{"var(--green)" if diff_months>0 else "var(--muted)"};'>
              {"🚀 加槓桿可提早 " + str(abs(diff_months)) + " 個月退休" if diff_months>0 else "兩方案相同"}
            </span>
          </div>
        </div>""", unsafe_allow_html=True)

        w1=mv8/total_mv if total_mv else 1/3
        w2=mv6/total_mv if total_mv else 1/3
        w3=mv3/total_mv if total_mv else 1/3
        blend=(w1*.08+w2*.14+w3*.10)*100

        st.markdown(f"""<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;'>
          <div class="card-green">
            <div class="lbl">退休月被動收入</div>
            <div style='font-family:Orbitron,monospace;font-size:1.5rem;color:var(--green);'>{show_val(monthly_passive)}</div>
            <div class="sub">{target_net/10000:.0f}萬 × {withdraw_rt:.1f}% ÷ 12</div>
            <div style='font-size:.72rem;color:var(--muted);margin-top:4px;'>✅ 免動用本金</div>
          </div>
          <div class="card">
            <div class="lbl">使用年化報酬率</div>
            <div style='font-family:Orbitron,monospace;font-size:1.5rem;color:var(--amber);'>{ret_rate}%</div>
            <div class="sub">加權混合：{blend:.1f}%</div>
            <div style='font-size:.72rem;color:var(--muted);margin-top:4px;'>含正2槓桿效益</div>
          </div>
          <div class="card">
            <div class="lbl">當前達標率</div>
            <div style='font-family:Orbitron,monospace;font-size:1.5rem;color:var(--cyan);'>{min(net_asset/target_net*100,100):.1f}%</div>
            <div class="sub">{show_val(net_asset)} / {fmtm(target_net)}</div>
            <div style='font-size:.72rem;color:var(--muted);margin-top:4px;'>尚差 {show_val(max(0,target_net-net_asset))}</div>
          </div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 5 — 定期定額
# ════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="sec">[ 07 ]  00631L 定期定額追蹤</div>', unsafe_allow_html=True)

    dc1, dc2 = st.columns([2,3])
    with dc1:
        st.markdown("##### ➕ 新增買入記錄")
        dca_date   = st.date_input("買入日期", value=date.today(), key="dca_d")
        dca_shares = st.number_input("買入股數", min_value=1, value=1000, step=100, key="dca_s")
        dca_price  = st.number_input("買入價格", min_value=0.01,
                                      value=round(float(p6),2) if p6 else 27.0,
                                      step=0.1, format="%.2f", key="dca_p")
        if st.button("➕  新增買入記錄", use_container_width=True):
            st.session_state.dca_records.append({
                "date":str(dca_date),"shares":dca_shares,
                "price":round(dca_price,2),"cost":round(dca_shares*dca_price)
            })
            st.session_state.dca_records.sort(key=lambda x: x["date"])
            save_all(); st.success("✅ 已新增")
        if st.session_state.dca_records:
            if st.button("🗑  刪除最後一筆", use_container_width=True):
                st.session_state.dca_records.pop(); save_all(); st.rerun()

    with dc2:
        recs = st.session_state.dca_records
        if recs:
            tot_sh=sum(r["shares"] for r in recs); tot_cost=sum(r["cost"] for r in recs)
            avg_p=tot_cost/tot_sh if tot_sh else 0
            cur_val=tot_sh*p6; pnl=cur_val-tot_cost
            pnl_pct=pnl/tot_cost*100 if tot_cost else 0
            pnl_col="var(--green)" if pnl>=0 else "var(--red)"
            tpct=min(cur_val/1_000_000*100,100)
            gap=max(0,1_000_000-cur_val)
            sugg=gap/18 if gap>0 else 0

            st.markdown(f"""<div class="card">
              <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px;'>
                <div><div class="lbl">平均成本</div>
                  <div class="med" style='color:var(--cyan);'>${avg_p:.2f}</div>
                  <div class="sub">現價 ${p6:.2f}</div></div>
                <div><div class="lbl">未實現損益</div>
                  <div class="med" style='color:{pnl_col};'>{show_val(pnl)}</div>
                  <div class="sub" style='color:{pnl_col};'>{pnl_pct:+.2f}%</div></div>
                <div><div class="lbl">持股市值</div>
                  <div class="med">{show_val(cur_val)}</div>
                  <div class="sub">{tot_sh:,} 股</div></div>
              </div>
              <div class="lbl">100萬目標進度</div>
              <div class="pbar-wrap"><div class="{'pbar-g' if tpct>=100 else 'pbar-a'}" style='width:{tpct:.1f}%;'></div></div>
              <div style='display:flex;justify-content:space-between;margin-bottom:10px;'>
                <span class="sml" style='color:var(--muted);'>{tpct:.1f}%</span>
                <span class="sml" style='color:var(--amber);'>{'🎯 達標！' if gap==0 else f"尚差 {show_val(gap)}"}</span>
              </div>
              <div style='background:#060d14;border:1px solid var(--border);border-radius:8px;padding:12px;'>
                <div class="lbl">建議每月定額（18個月達標）</div>
                <div class="med" style='color:var(--amber);'>{fmt(sugg)}</div>
                <div class="sub">總成本 {show_val(tot_cost)} · 共 {len(recs)} 筆</div>
              </div>
            </div>""", unsafe_allow_html=True)

            with st.expander(f"📋 買入記錄（共 {len(recs)} 筆）"):
                rows=""
                for r in reversed(recs):
                    rv=r["shares"]*p6; rpnl=rv-r["cost"]
                    rc2_="var(--green)" if rpnl>=0 else "var(--red)"
                    rows+=f"""<tr style='border-bottom:1px solid var(--border);'>
                      <td style='padding:8px 12px;font-family:Share Tech Mono,monospace;color:var(--cyan);font-size:.82rem;'>{r['date']}</td>
                      <td style='padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:.82rem;text-align:right;'>{r['shares']:,}</td>
                      <td style='padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:.82rem;text-align:right;'>${r['price']:.2f}</td>
                      <td style='padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:.82rem;text-align:right;'>{show_val(r['cost'])}</td>
                      <td style='padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:.82rem;text-align:right;color:{rc2_};'>{show_val(rpnl)}</td>
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
            st.markdown('<div class="card" style="text-align:center;padding:32px;color:var(--muted);">尚無記錄，從左側新增第一筆</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 6 — 收入配置
# ════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="sec">[ 08 ]  收入配置計算機</div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["💼 月薪配置", "🎁 獎金配置（5/1 績效 ＆ 1/1 年終）"])

    with t1:
        ic1, ic2 = st.columns([2,3])
        with ic1:
            net_sal2  = st.number_input("月薪實領", 0, value=63000, step=1000, key="sal2_net")
            dca_a     = st.number_input("定期定額 00631L", 0, value=38000, step=1000, key="sal2_dca")
            rent2     = st.number_input("房租/房貸", 0, value=12000, step=500,  key="sal2_rent")
            ins2      = st.number_input("保險費",    0, value=2500,  step=100,  key="sal2_ins")
            phone2    = st.number_input("電信費",    0, value=999,   step=1,    key="sal2_ph")
            sub2      = st.number_input("訂閱/固定", 0, value=500,   step=100,  key="sal2_sub")
            food2     = st.number_input("飲食/日常", 0, value=8000,  step=500,  key="sal2_food")
            fun2      = st.number_input("娛樂/聚餐", 0, value=6000,  step=500,  key="sal2_fun")
        with ic2:
            rigid2=rent2+ins2+phone2+sub2; living2=food2+fun2
            out2=dca_a+rigid2+living2+round(monthly_int)
            sur2=net_sal2-out2; sc_="var(--green)" if sur2>=0 else "var(--red)"
            up2=min(out2/net_sal2*100,100) if net_sal2 else 0
            items2=[("📈 定期定額",dca_a,"var(--green)","複利引擎"),
                    ("🏠 剛性支出",rigid2,"var(--red)",f"房{rent2:,} 險{ins2:,} 電{phone2:,} 訂{sub2:,}"),
                    ("🛒 生活費",living2,"var(--cyan)",f"食{food2:,} 樂{fun2:,}"),
                    ("🏦 質押息",round(monthly_int),"#ff7799",f"{pledge_rate:.2f}%")]
            rows2=""
            for n,a,c,nt in items2:
                pp=a/net_sal2*100 if net_sal2 else 0
                rows2+=f"""<tr style='border-bottom:1px solid var(--border);'>
                  <td style='padding:9px 12px;font-size:.9rem;color:{c};'>{n}</td>
                  <td style='padding:9px 12px;font-family:Share Tech Mono,monospace;font-size:.9rem;text-align:right;'>{fmt(a)}</td>
                  <td style='padding:9px 12px;font-family:Share Tech Mono,monospace;font-size:.82rem;color:var(--muted);text-align:right;'>{pp:.1f}%</td>
                  <td style='padding:9px 12px;font-size:.75rem;color:var(--dim);'>{nt}</td>
                </tr>"""
            adv="💡 結餘建議加碼" if sur2>0 else f"⚠ 超支 {fmt(abs(sur2))}"
            st.markdown(f"""<div class="card">
              <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px;'>
                <div><div class="lbl">月薪</div><div class="med" style='color:var(--cyan);'>{fmt(net_sal2)}</div></div>
                <div><div class="lbl">總支出</div><div class="med" style='color:var(--amber);'>{fmt(out2)}</div><div class="sub">{up2:.1f}%</div></div>
                <div><div class="lbl">本月結餘</div><div class="med" style='color:{sc_};'>{fmt(sur2)}</div></div>
              </div>
              <div class="pbar-wrap"><div class="{'pbar-g' if sur2>=0 else 'pbar-r'}" style='width:{up2:.1f}%;'></div></div>
              <table style='width:100%;border-collapse:collapse;margin-top:12px;'>
                <thead><tr style='border-bottom:2px solid var(--border);'>
                  <th style='padding:9px 12px;font-size:.72rem;color:var(--muted);text-align:left;'>項目</th>
                  <th style='padding:9px 12px;font-size:.72rem;color:var(--muted);text-align:right;'>金額</th>
                  <th style='padding:9px 12px;font-size:.72rem;color:var(--muted);text-align:right;'>佔薪</th>
                  <th style='padding:9px 12px;font-size:.72rem;color:var(--muted);text-align:left;'>說明</th>
                </tr></thead>
                <tbody>{rows2}</tbody>
                <tfoot><tr style='border-top:2px solid var(--border);'>
                  <td style='padding:10px 12px;font-size:.9rem;color:var(--cyan);font-weight:bold;'>本月結餘</td>
                  <td style='padding:10px 12px;font-family:Share Tech Mono,monospace;font-size:1rem;color:{sc_};text-align:right;font-weight:bold;'>{fmt(sur2)}</td>
                  <td colspan='2' style='padding:10px 12px;font-size:.8rem;color:{sc_};'>{adv}</td>
                </tfoot>
              </table>
            </div>""", unsafe_allow_html=True)

    with t2:
        bc1, bc2 = st.columns([2,3])
        with bc1:
            b_type  = st.selectbox("獎金類型", ["🎁 績效獎金（5月1日）","🎊 年終獎金（1月1日）"], key="b2_type")
            b_gross = st.number_input("稅前金額", 0, value=113405, step=1000, key="b2_gross")
            b_tax   = st.number_input("稅率 (%)", 0, 40, value=10, step=1, key="b2_tax")
            dream_fund = st.number_input("🌟 夢想金（保留享樂）", 0, value=50000, step=5000, key="b2_dream",
                                          help="固定保留這筆錢犒賞自己，剩餘才投資")
            b_pledge2 = st.number_input("提前還質押", 0, value=0, step=10000, key="b2_pledge")
            b_save2   = st.number_input("定存/備用", 0, value=0, step=5000, key="b2_save")

        with bc2:
            after2   = round(b_gross*(1-b_tax/100))
            for_invest = max(0, after2 - dream_fund - b_pledge2 - b_save2)
            total_a2 = dream_fund + b_pledge2 + b_save2 + for_invest
            unalloc2 = after2 - total_a2
            int_sv2  = b_pledge2*pledge_rate/100
            new_mv6  = mv6 + for_invest
            new_pct6 = min(new_mv6/1_000_000*100,100)
            bp2      = min(total_a2/after2*100,100) if after2 else 0

            m_after=0; v2=new_mv6
            while v2<1_000_000 and m_after<120: v2+=monthly_inv; m_after+=1

            st.markdown(f"""<div class="card">
              <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:14px;'>
                <div><div class="lbl">稅後到手</div>
                  <div class="med" style='color:var(--cyan);'>{fmt(after2)}</div>
                  <div class="sub">扣 {b_tax}% 稅</div></div>
                <div><div class="lbl">🌟 夢想金</div>
                  <div class="med" style='color:var(--purple);'>{fmt(dream_fund)}</div>
                  <div class="sub">犒賞自己</div></div>
                <div><div class="lbl">加碼投資</div>
                  <div class="med" style='color:var(--green);'>{fmt(for_invest)}</div>
                  <div class="sub">自動分配剩餘</div></div>
              </div>
              <div class="pbar-wrap"><div class="pbar-g" style='width:{bp2:.1f}%;'></div></div>
              <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px;'>
                <div style='background:#060d14;border:1px solid var(--border);border-radius:8px;padding:12px;'>
                  <div class="lbl">加碼後 00631L 進度</div>
                  <div class="med" style='color:var(--green);'>{new_pct6:.1f}%</div>
                  <div class="pbar-wrap"><div class="pbar-g" style='width:{new_pct6:.1f}%;'></div></div>
                  <div class="sub">{fmt(new_mv6)} / $1,000,000</div>
                  <div style='font-size:.75rem;color:var(--muted);margin-top:4px;'>再 <span style='color:var(--amber);'>{m_after} 個月</span>達標</div>
                </div>
                <div style='background:#060d14;border:1px solid var(--border);border-radius:8px;padding:12px;'>
                  <div class="lbl">分配明細</div>
                  <div style='font-size:.82rem;color:var(--muted);line-height:2;margin-top:4px;'>
                    🌟 夢想金 <span style='color:var(--purple);font-family:Share Tech Mono,monospace;'>{fmt(dream_fund)}</span><br>
                    📈 加碼投資 <span style='color:var(--green);font-family:Share Tech Mono,monospace;'>{fmt(for_invest)}</span><br>
                    🏦 還款省息 <span style='color:var(--cyan);font-family:Share Tech Mono,monospace;'>{fmt(int_sv2)}/年</span><br>
                    💰 定存備用 <span style='color:var(--muted);font-family:Share Tech Mono,monospace;'>{fmt(b_save2)}</span>
                  </div>
                </div>
              </div>
              <div style='margin-top:12px;padding:10px 14px;background:#060d14;border:1px solid var(--border);border-radius:8px;
                          font-size:.78rem;color:var(--muted);line-height:2;'>
                ① 先留夢想金 {fmt(dream_fund)}，不虧待自己<br>
                ② 剩餘 {fmt(for_invest)} 全加碼 00631L，加速 100 萬目標<br>
                ③ 達標後轉入 006208 擴大質押槓桿
              </div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STRATEGY SOP
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
with st.expander("📋  F.I.R.E 策略 SOP"):
    st.markdown("""
    <div style='font-family:Share Tech Mono,monospace;font-size:.85rem;color:var(--muted);line-height:2.3;padding:4px 0;'>
      <span style='color:var(--cyan);'>PHASE 1</span> &nbsp;每月定期定額 00631L，累積至市值 ≥ 100萬<br>
      <span style='color:var(--cyan);'>PHASE 2</span> &nbsp;達標後賣出，轉入 006208，建立質押部位<br>
      <span style='color:var(--cyan);'>PHASE 3</span> &nbsp;維持質押率 ≥ 250%，借出資金持續買入 2330<br>
      <span style='color:var(--amber);'>加碼時機</span> &nbsp;5/1 績效獎金 ＆ 1/1 年終獎金優先加碼，扣除夢想金後全押<br>
      <span style='color:var(--red);'>風控底線</span> &nbsp;質押維持率 &lt; 220% 立即補倉或還款 · 永遠保留緊急備用金
    </div>
    """, unsafe_allow_html=True)

# FOOTER
now_str2 = datetime.now().strftime("%Y-%m-%d %H:%M")
st.markdown(f"""
<div style='text-align:center;padding:18px 0 6px;border-top:1px solid var(--border);margin-top:12px;'>
  <span style='font-family:Share Tech Mono,monospace;font-size:.62rem;color:var(--dim);letter-spacing:.12em;'>
    PROJECT F.I.R.E &nbsp;│&nbsp; NOT FINANCIAL ADVICE &nbsp;│&nbsp; {now_str2}
  </span>
</div>""", unsafe_allow_html=True)
