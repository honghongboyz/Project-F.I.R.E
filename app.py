import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, date, timedelta
import time

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
# GLOBAL CSS — Bloomberg Terminal Meets Cyberpunk
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@700;900&display=swap');

:root {
    --bg-base:      #080c10;
    --bg-panel:     #0d1117;
    --bg-card:      #111820;
    --bg-card2:     #0a1520;
    --border:       #1e3a4a;
    --border-glow:  #00d4ff33;
    --accent-cyan:  #00d4ff;
    --accent-green: #00ff88;
    --accent-red:   #ff3366;
    --accent-amber: #ffaa00;
    --text-primary: #e8f4f8;
    --text-muted:   #5a7a8a;
    --text-dim:     #2a4a5a;
    --font-mono:    'Share Tech Mono', monospace;
    --font-display: 'Orbitron', monospace;
    --font-body:    'Rajdhani', sans-serif;
}

html, body, [data-testid="stApp"] {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050810 0%, #080d14 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
}
[data-testid="stSidebar"] .stNumberInput input,
[data-testid="stSidebar"] .stDateInput input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--accent-cyan) !important;
    font-family: var(--font-mono) !important;
    border-radius: 4px !important;
}
[data-testid="stSidebar"] label {
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] h3 {
    color: var(--accent-cyan) !important;
    font-family: var(--font-display) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.2em !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 6px !important;
    margin-top: 16px !important;
}

/* Main content area */
[data-testid="block-container"] { padding-top: 1rem !important; }
.stMarkdown p { font-family: var(--font-body); color: var(--text-primary); }
hr { border-color: var(--border) !important; margin: 0.5rem 0 !important; }

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    box-shadow: 0 0 20px var(--border-glow) !important;
}
[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-mono) !important;
    font-size: 1.4rem !important;
    color: var(--accent-cyan) !important;
}
[data-testid="stMetricDelta"] {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
}

/* Divider */
.fire-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1rem 0;
    box-shadow: 0 1px 0 var(--border-glow);
}

/* Section headers */
.section-header {
    font-family: var(--font-display);
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: var(--accent-cyan);
    text-transform: uppercase;
    padding: 4px 0 8px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}

/* Ticker cards */
.ticker-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 30px rgba(0,212,255,0.05);
    transition: border-color 0.2s;
}
.ticker-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-cyan), transparent);
}
.ticker-symbol {
    font-family: var(--font-display);
    font-size: 1rem;
    color: var(--accent-cyan);
    letter-spacing: 0.1em;
}
.ticker-name {
    font-family: var(--font-body);
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 2px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.ticker-price {
    font-family: var(--font-mono);
    font-size: 1.8rem;
    color: var(--text-primary);
    margin: 8px 0 4px 0;
    line-height: 1;
}
.ticker-value {
    font-family: var(--font-mono);
    font-size: 0.85rem;
    color: var(--accent-green);
}
.ticker-shares {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-top: 4px;
}
.ticker-status-live {
    display: inline-block;
    background: var(--accent-green);
    color: #000;
    font-family: var(--font-mono);
    font-size: 0.55rem;
    padding: 1px 6px;
    border-radius: 2px;
    letter-spacing: 0.1em;
    font-weight: bold;
    animation: blink 2s infinite;
}
.ticker-status-close {
    display: inline-block;
    background: var(--text-muted);
    color: #000;
    font-family: var(--font-mono);
    font-size: 0.55rem;
    padding: 1px 6px;
    border-radius: 2px;
    letter-spacing: 0.1em;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* Alert cards */
.alert-card-red {
    background: linear-gradient(135deg, #1a0010, #200818);
    border: 2px solid var(--accent-red);
    border-radius: 8px;
    padding: 16px 20px;
    box-shadow: 0 0 30px rgba(255,51,102,0.3), inset 0 0 40px rgba(255,51,102,0.05);
    animation: pulse-red 2s infinite;
}
.alert-card-green {
    background: var(--bg-card);
    border: 1px solid var(--accent-green);
    border-radius: 8px;
    padding: 16px 20px;
    box-shadow: 0 0 15px rgba(0,255,136,0.1);
}
.alert-card-amber {
    background: linear-gradient(135deg, #150e00, #1a1200);
    border: 1px solid var(--accent-amber);
    border-radius: 8px;
    padding: 16px 20px;
    box-shadow: 0 0 15px rgba(255,170,0,0.15);
}
.alert-card-neutral {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
}
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 30px rgba(255,51,102,0.3); }
    50% { box-shadow: 0 0 50px rgba(255,51,102,0.6); }
}

/* Progress bar */
.progress-wrap {
    background: var(--bg-base);
    border: 1px solid var(--border);
    border-radius: 4px;
    height: 8px;
    margin: 8px 0;
    overflow: hidden;
}
.progress-fill-green {
    background: linear-gradient(90deg, var(--accent-green), #00ffcc);
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
    box-shadow: 0 0 10px var(--accent-green);
}
.progress-fill-amber {
    background: linear-gradient(90deg, var(--accent-amber), #ffcc44);
    height: 100%;
    border-radius: 4px;
    box-shadow: 0 0 10px var(--accent-amber);
}
.progress-fill-red {
    background: linear-gradient(90deg, var(--accent-red), #ff6688);
    height: 100%;
    border-radius: 4px;
    box-shadow: 0 0 10px var(--accent-red);
}

/* KPI number display */
.kpi-num {
    font-family: var(--font-mono);
    font-size: 1.6rem;
    font-weight: 700;
    line-height: 1.1;
}
.kpi-label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 6px;
}
.kpi-sub {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 4px;
}

/* Retirement card */
.retirement-card {
    background: linear-gradient(135deg, var(--bg-card2), var(--bg-card));
    border: 1px solid #1a3a5a;
    border-radius: 10px;
    padding: 24px 28px;
    box-shadow: 0 0 40px rgba(0,212,255,0.08);
    position: relative;
    overflow: hidden;
}
.retirement-card::after {
    content: '🔥';
    position: absolute;
    bottom: -10px;
    right: 10px;
    font-size: 5rem;
    opacity: 0.05;
}
.retirement-date {
    font-family: var(--font-display);
    font-size: 2rem;
    color: var(--accent-cyan);
    letter-spacing: 0.05em;
}
.retirement-age {
    font-family: var(--font-display);
    font-size: 1.2rem;
    color: var(--accent-green);
}

/* Net asset hero */
.net-asset-hero {
    background: linear-gradient(135deg, #050d18 0%, #081520 100%);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 28px;
    text-align: center;
    box-shadow: 0 0 60px rgba(0,212,255,0.07);
}
.net-asset-num {
    font-family: var(--font-display);
    font-size: 2.4rem;
    color: var(--accent-cyan);
    letter-spacing: 0.05em;
    text-shadow: 0 0 20px rgba(0,212,255,0.4);
}

/* Timestamp */
.ts-badge {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-dim);
    letter-spacing: 0.1em;
}

/* Button styling */
.stButton button {
    background: var(--bg-card) !important;
    border: 1px solid var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 4px !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    background: rgba(0,212,255,0.1) !important;
    box-shadow: 0 0 15px rgba(0,212,255,0.3) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* Expander */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
details summary {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    color: var(--accent-cyan) !important;
    letter-spacing: 0.1em !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch_price(ticker_tw: str) -> dict:
    """Fetch real-time or latest close price for a TW stock."""
    symbol = ticker_tw + ".TW"
    result = {"price": None, "prev_close": None, "is_live": False, "error": None}
    try:
        tkr = yf.Ticker(symbol)
        info = tkr.fast_info
        price = getattr(info, "last_price", None)
        prev = getattr(info, "previous_close", None)

        if price is None or price == 0:
            hist = tkr.history(period="5d")
            if not hist.empty:
                price = float(hist["Close"].iloc[-1])
                prev  = float(hist["Close"].iloc[-2]) if len(hist) > 1 else price
                result["is_live"] = False
            else:
                result["error"] = "No data"
                return result
        else:
            result["is_live"] = True

        result["price"]      = float(price)
        result["prev_close"] = float(prev) if prev else float(price)
    except Exception as e:
        result["error"] = str(e)
    return result


def fmt_twd(val: float, decimals: int = 0) -> str:
    if decimals == 0:
        return f"${val:,.0f}"
    return f"${val:,.{decimals}f}"


def fmt_pct(val: float) -> str:
    return f"{val:.2f}%"


def calc_change_pct(price, prev) -> float:
    if prev and prev != 0:
        return (price - prev) / prev * 100
    return 0.0


def months_to_retirement(
    current_net: float,
    target_net: float,
    monthly_invest: float,
    val_006208: float,
    val_00631L: float,
    val_2330: float,
    total_market_val: float,
    pledge_loan: float,
) -> int:
    """Simulate month-by-month until net asset >= target."""
    if total_market_val <= 0:
        w1 = w2 = w3 = 1/3
    else:
        w1 = val_006208 / total_market_val
        w2 = val_00631L / total_market_val
        w3 = val_2330   / total_market_val

    blended_annual = w1 * 0.08 + w2 * 0.14 + w3 * 0.10
    monthly_rate   = (1 + blended_annual) ** (1/12) - 1

    net = current_net
    months = 0
    MAX_MONTHS = 600  # 50 years cap

    while net < target_net and months < MAX_MONTHS:
        net = net * (1 + monthly_rate) + monthly_invest
        months += 1

    return months


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 16px 0;'>
        <div style='font-family:"Orbitron",monospace; font-size:1rem; color:#00d4ff; letter-spacing:0.2em;'>
            🔥 F.I.R.E
        </div>
        <div style='font-family:"Share Tech Mono",monospace; font-size:0.6rem; color:#2a4a5a; letter-spacing:0.15em; margin-top:4px;'>
            FINANCIAL INDEPENDENCE RETIRE EARLY
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 持股數量")
    shares_006208 = st.number_input("006208 持股 (股)", min_value=0, value=10000, step=100, key="s1")
    shares_00631L = st.number_input("00631L 持股 (股)", min_value=0, value=5000, step=100, key="s2")
    shares_2330   = st.number_input("2330 持股 (股)",   min_value=0, value=200,   step=10,  key="s3")

    st.markdown("### 🏦 質押條件")
    pledge_loan = st.number_input(
        "質押借款總額 (TWD)", min_value=0, value=1_500_000, step=10_000,
        help="目前向券商借出的總金額"
    )
    pledge_rate = st.number_input(
        "質押年利率 (%)", min_value=0.0, value=2.4, step=0.1, format="%.2f"
    )
    pledge_expiry = st.date_input(
        "借款到期日",
        value=date.today() + timedelta(days=180),
        min_value=date.today(),
    )

    st.markdown("### 🎯 退休目標")
    target_net = st.number_input(
        "目標淨資產 (TWD)", min_value=1_000_000, value=30_000_000, step=500_000
    )
    monthly_invest = st.number_input(
        "每月定額投入 (TWD)", min_value=0, value=30_000, step=1_000
    )
    withdrawal_rate = st.number_input(
        "安全提領率 (%)", min_value=1.0, max_value=10.0, value=4.0, step=0.1, format="%.1f"
    )
    dob = st.date_input(
        "出生年月日",
        value=date(1992, 12, 14),
        min_value=date(1950, 1, 1),
        max_value=date.today() - timedelta(days=365*18),
    )

    st.markdown("---")
    refresh_btn = st.button("⟳  REFRESH PRICES", use_container_width=True)


# ─────────────────────────────────────────────
# FETCH PRICES
# ─────────────────────────────────────────────
if refresh_btn:
    st.cache_data.clear()

with st.spinner(""):
    d006208 = fetch_price("006208")
    d00631L = fetch_price("00631L")
    d2330   = fetch_price("2330")


def safe_price(d): return d["price"] or 0.0
def safe_prev(d):  return d["prev_close"] or safe_price(d)

p_006208 = safe_price(d006208)
p_00631L = safe_price(d00631L)
p_2330   = safe_price(d2330)

# Market values
mv_006208 = p_006208 * shares_006208
mv_00631L = p_00631L * shares_00631L
mv_2330   = p_2330   * shares_2330

total_mv  = mv_006208 + mv_00631L + mv_2330
net_asset = total_mv - pledge_loan

# Interest
annual_interest = pledge_loan * pledge_rate / 100
monthly_interest = annual_interest / 12

# Days to expiry
days_to_expiry = (pledge_expiry - date.today()).days

# Pledge maintenance ratio
if pledge_loan > 0:
    pledge_ratio = (mv_006208 / pledge_loan) * 100
else:
    pledge_ratio = 9999.0

# Extra borrowing capacity (at 250% ratio)
extra_borrow = (mv_006208 / 2.5) - pledge_loan

# 00631L conversion progress
conversion_pct = min((mv_00631L / 1_000_000) * 100, 100) if mv_00631L > 0 else 0.0
conversion_trigger = mv_00631L >= 1_000_000


# ─────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────
now_str = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

st.markdown(f"""
<div style='padding: 6px 0 18px 0;'>
    <div style='display:flex; align-items:baseline; gap:16px; flex-wrap:wrap;'>
        <span style='font-family:"Orbitron",monospace; font-size:1.7rem; color:#00d4ff;
                     letter-spacing:0.12em; text-shadow:0 0 30px rgba(0,212,255,0.5);'>
            PROJECT F.I.R.E
        </span>
        <span style='font-family:"Orbitron",monospace; font-size:0.6rem; color:#1e3a4a;
                     letter-spacing:0.25em; padding-top:4px;'>
            DASHBOARD
        </span>
    </div>
    <div style='font-family:"Share Tech Mono",monospace; font-size:0.62rem; color:#2a4a5a;
                letter-spacing:0.18em; margin-top:4px;'>
        FINANCIAL INDEPENDENCE · RETIRE EARLY &nbsp;│&nbsp; LAST UPDATE: {now_str}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="fire-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ROW 1 — TICKER CARDS
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">[ 01 ]  即時報價 · LIVE QUOTES</div>', unsafe_allow_html=True)

NAMES = {
    "006208": "富邦台50 ETF",
    "00631L": "富邦台灣50正2 ETF",
    "2330":   "台積電 TSMC",
}

def ticker_card_html(symbol, name, price_d, shares, mv):
    p     = safe_price(price_d)
    prev  = safe_prev(price_d)
    chg   = calc_change_pct(p, prev)
    chg_abs = p - prev
    is_live = price_d["is_live"]
    err     = price_d["error"]

    status_html = (
        '<span class="ticker-status-live">● LIVE</span>'
        if is_live and not err
        else '<span class="ticker-status-close">■ CLOSE</span>'
    )
    if err:
        status_html += f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:0.6rem;color:#ff3366;margin-left:8px;">ERR: {err[:30]}</span>'

    chg_color = "#00ff88" if chg >= 0 else "#ff3366"
    chg_icon  = "▲" if chg >= 0 else "▼"

    return f"""
    <div class="ticker-card">
        <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
            <div>
                <div class="ticker-symbol">{symbol}</div>
                <div class="ticker-name">{name}</div>
            </div>
            <div>{status_html}</div>
        </div>
        <div class="ticker-price">
            <span style='color:#e8f4f8;'>{p:,.2f}</span>
            <span style='font-size:0.85rem;color:#5a7a8a;margin-left:4px;'>TWD</span>
        </div>
        <div style='font-family:"Share Tech Mono",monospace;font-size:0.78rem;color:{chg_color};'>
            {chg_icon} {chg_abs:+.2f} &nbsp; ({chg:+.2f}%)
        </div>
        <hr style='border-color:#1e3a4a;margin:8px 0;'>
        <div class="ticker-value">{fmt_twd(mv)}</div>
        <div class="ticker-shares">{shares:,} 股 ×  {p:,.2f}</div>
    </div>
    """

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(ticker_card_html("006208", NAMES["006208"], d006208, shares_006208, mv_006208), unsafe_allow_html=True)
with col2:
    st.markdown(ticker_card_html("00631L", NAMES["00631L"], d00631L, shares_00631L, mv_00631L), unsafe_allow_html=True)
with col3:
    st.markdown(ticker_card_html("2330",   NAMES["2330"],   d2330,   shares_2330,   mv_2330),   unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ROW 2 — NET ASSET SUMMARY
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="section-header">[ 02 ]  總資產結算 · NET ASSET SUMMARY</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("總市值", fmt_twd(total_mv), delta=None)
with c2:
    st.metric("質押借款", fmt_twd(pledge_loan), delta=None)
with c3:
    st.metric("總淨資產", fmt_twd(net_asset), delta=f"{(net_asset/target_net*100):.1f}% of target")
with c4:
    st.metric("距借款到期", f"{days_to_expiry} 天", delta=None)

# Interest row
c5, c6, c7, c8 = st.columns(4)
with c5:
    st.metric("年利率", fmt_pct(pledge_rate), delta=None)
with c6:
    st.metric("年利息支出", fmt_twd(annual_interest), delta=None)
with c7:
    st.metric("月利息支出", fmt_twd(monthly_interest), delta=None)
with c8:
    expiry_str = pledge_expiry.strftime("%Y/%m/%d")
    days_color = "normal" if days_to_expiry > 60 else "inverse"
    st.metric("到期日", expiry_str, delta=f"{'⚠ 注意' if days_to_expiry <= 60 else '安全'}")


# ─────────────────────────────────────────────
# ROW 3 — CORE MONITORING
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="section-header">[ 03 ]  核心監控 · CORE MONITORING</div>', unsafe_allow_html=True)

mon_c1, mon_c2, mon_c3 = st.columns(3)

# ── 00631L Conversion Monitor ──
with mon_c1:
    if conversion_trigger:
        bar_color = "progress-fill-red"
        card_class = "alert-card-red"
        conv_label = "🚨 執行轉換"
        conv_msg   = "市值已達 ≥ 100 萬，請立即賣出 00631L 轉入 006208！"
        conv_color = "#ff3366"
        pct_display = f"100.0%"
    else:
        bar_color = "progress-fill-green" if conversion_pct >= 70 else "progress-fill-amber"
        card_class = "alert-card-neutral"
        conv_label = "進行中"
        conv_msg   = f"距目標尚差 {fmt_twd(max(0, 1_000_000 - mv_00631L))}"
        conv_color = "#00ff88"
        pct_display = f"{conversion_pct:.1f}%"

    st.markdown(f"""
    <div class="{card_class}">
        <div class="kpi-label">00631L 轉換進度</div>
        <div class="kpi-num" style='color:{conv_color};'>{pct_display}</div>
        <div class="progress-wrap">
            <div class="{bar_color}" style='width:{min(conversion_pct,100):.1f}%;'></div>
        </div>
        <div style='display:flex;justify-content:space-between;'>
            <span style='font-family:"Share Tech Mono",monospace;font-size:0.7rem;color:#5a7a8a;'>
                {fmt_twd(mv_00631L)} / 1,000,000
            </span>
            <span style='font-family:"Share Tech Mono",monospace;font-size:0.7rem;color:{conv_color};
                         {"font-weight:bold;" if conversion_trigger else ""}'>
                {conv_label}
            </span>
        </div>
        <div style='font-family:"Share Tech Mono",monospace;font-size:0.65rem;color:{conv_color};
                    margin-top:8px;{"animation:blink 1s infinite;" if conversion_trigger else ""}'>
            {conv_msg}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Pledge Maintenance Ratio ──
with mon_c2:
    if pledge_loan == 0:
        ratio_color = "#00ff88"
        ratio_class = "alert-card-green"
        ratio_label = "無借款"
        ratio_bar   = "progress-fill-green"
        ratio_msg   = "目前無質押借款"
        ratio_pct_bar = 100
    elif pledge_ratio < 220:
        ratio_color = "#ff3366"
        ratio_class = "alert-card-red"
        ratio_label = "⚠ 危險"
        ratio_bar   = "progress-fill-red"
        ratio_msg   = f"低於 220% 強制回補線！現為 {pledge_ratio:.1f}%"
        ratio_pct_bar = min(pledge_ratio / 3.5, 100)
    elif pledge_ratio < 250:
        ratio_color = "#ffaa00"
        ratio_class = "alert-card-amber"
        ratio_label = "注意"
        ratio_bar   = "progress-fill-amber"
        ratio_msg   = f"介於 220–250%，建議補充擔保品"
        ratio_pct_bar = min(pledge_ratio / 3.5, 100)
    else:
        ratio_color = "#00ff88"
        ratio_class = "alert-card-green"
        ratio_label = "安全"
        ratio_bar   = "progress-fill-green"
        ratio_msg   = f"維持率充足，策略安全運行中"
        ratio_pct_bar = min(pledge_ratio / 3.5, 100)

    st.markdown(f"""
    <div class="{ratio_class}">
        <div class="kpi-label">006208 質押維持率</div>
        <div class="kpi-num" style='color:{ratio_color};'>
            {pledge_ratio:.1f if pledge_loan > 0 else '∞'}<span style='font-size:1rem;'>%</span>
        </div>
        <div class="progress-wrap">
            <div class="{ratio_bar}" style='width:{ratio_pct_bar:.1f}%;'></div>
        </div>
        <div style='display:flex;justify-content:space-between;'>
            <span style='font-family:"Share Tech Mono",monospace;font-size:0.65rem;color:#5a7a8a;'>
                警戒 220% &nbsp;│&nbsp; 安全 250%
            </span>
            <span style='font-family:"Share Tech Mono",monospace;font-size:0.7rem;color:{ratio_color};'>
                {ratio_label}
            </span>
        </div>
        <div style='font-family:"Share Tech Mono",monospace;font-size:0.65rem;color:{ratio_color};margin-top:8px;'>
            {ratio_msg}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Extra Borrowing Capacity ──
with mon_c3:
    borrow_color = "#00ff88" if extra_borrow >= 0 else "#ff3366"
    borrow_class = "alert-card-green" if extra_borrow >= 0 else "alert-card-red"
    borrow_label = "可增貸" if extra_borrow >= 0 else "需補擔保"

    # Max borrowable at 250%
    max_borrow = mv_006208 / 2.5 if mv_006208 > 0 else 0
    borrow_used_pct = (pledge_loan / max_borrow * 100) if max_borrow > 0 else 0

    st.markdown(f"""
    <div class="{borrow_class}">
        <div class="kpi-label">可增貸空間 (at 250% ratio)</div>
        <div class="kpi-num" style='color:{borrow_color};'>{fmt_twd(abs(extra_borrow))}</div>
        <div class="progress-wrap">
            <div class="progress-fill-{'green' if extra_borrow >= 0 else 'red'}"
                 style='width:{min(borrow_used_pct, 100):.1f}%;'></div>
        </div>
        <div style='display:flex;justify-content:space-between;'>
            <span style='font-family:"Share Tech Mono",monospace;font-size:0.65rem;color:#5a7a8a;'>
                已借 {fmt_twd(pledge_loan)} / 上限 {fmt_twd(max_borrow)}
            </span>
            <span style='font-family:"Share Tech Mono",monospace;font-size:0.7rem;color:{borrow_color};'>
                {borrow_label}
            </span>
        </div>
        <div style='font-family:"Share Tech Mono",monospace;font-size:0.65rem;color:#5a7a8a;margin-top:8px;'>
            006208 市值 {fmt_twd(mv_006208)} ÷ 2.5 = 上限 {fmt_twd(max_borrow)}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ROW 4 — RETIREMENT PROJECTION
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="section-header">[ 04 ]  退休預估 · DYNAMIC RETIREMENT PROJECTION</div>', unsafe_allow_html=True)

months_needed = months_to_retirement(
    current_net=net_asset,
    target_net=target_net,
    monthly_invest=monthly_invest,
    val_006208=mv_006208,
    val_00631L=mv_00631L,
    val_2330=mv_2330,
    total_market_val=total_mv,
    pledge_loan=pledge_loan,
)

retire_date = datetime.now() + timedelta(days=months_needed * 30.44)
retire_date_str = retire_date.strftime("%Y 年 %m 月")

# Age at retirement
dob_dt = datetime(dob.year, dob.month, dob.day)
retire_age_days = (retire_date - dob_dt).days
retire_age = retire_age_days / 365.25

# Monthly passive income
monthly_passive = (target_net * withdrawal_rate / 100) / 12

# Years & months breakdown
years_needed  = months_needed // 12
months_remain = months_needed % 12

# Blended rate display
if total_mv > 0:
    w1 = mv_006208 / total_mv
    w2 = mv_00631L / total_mv
    w3 = mv_2330   / total_mv
else:
    w1 = w2 = w3 = 1/3
blended_rate = (w1 * 0.08 + w2 * 0.14 + w3 * 0.10) * 100

ret_c1, ret_c2 = st.columns([3, 2])

with ret_c1:
    st.markdown(f"""
    <div class="retirement-card">
        <div class="kpi-label" style='margin-bottom:12px;'>預估財務自由日</div>
        <div class="retirement-date">{retire_date_str}</div>
        <div class="retirement-age" style='margin-top:8px;'>屆時年齡：{retire_age:.1f} 歲</div>
        <hr style='border-color:#1a3a5a;margin:16px 0;'>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:16px;'>
            <div>
                <div class="kpi-label">距今月數</div>
                <div style='font-family:"Share Tech Mono",monospace;font-size:1.1rem;color:#e8f4f8;'>
                    {months_needed} 個月
                </div>
                <div style='font-family:"Share Tech Mono",monospace;font-size:0.7rem;color:#5a7a8a;'>
                    ({years_needed} 年 {months_remain} 個月)
                </div>
            </div>
            <div>
                <div class="kpi-label">混合年化報酬率</div>
                <div style='font-family:"Share Tech Mono",monospace;font-size:1.1rem;color:#00d4ff;'>
                    {blended_rate:.2f}%
                </div>
                <div style='font-family:"Share Tech Mono",monospace;font-size:0.65rem;color:#5a7a8a;'>
                    加權平均估算
                </div>
            </div>
        </div>
        <hr style='border-color:#1a3a5a;margin:16px 0;'>
        <div style='font-family:"Share Tech Mono",monospace;font-size:0.65rem;color:#2a4a5a;'>
            假設：006208 年化 8% · 00631L 年化 14% · 2330 年化 10%<br>
            每月定投 {fmt_twd(monthly_invest)} · 目標淨資產 {fmt_twd(target_net)}
        </div>
    </div>
    """, unsafe_allow_html=True)

with ret_c2:
    st.markdown(f"""
    <div style='display:flex;flex-direction:column;gap:12px;height:100%;'>
        <div class="alert-card-green" style='flex:1;'>
            <div class="kpi-label">預估退休月生活費</div>
            <div style='font-family:"Orbitron",monospace;font-size:1.8rem;color:#00ff88;
                        text-shadow:0 0 20px rgba(0,255,136,0.4);margin:8px 0;'>
                {fmt_twd(monthly_passive)}
            </div>
            <div style='font-family:"Share Tech Mono",monospace;font-size:0.65rem;color:#5a7a8a;
                        line-height:1.5;'>
                {fmt_twd(target_net)} × {withdrawal_rate:.1f}% ÷ 12<br>
                ✓ 免動用本金之純被動收入<br>
                ✓ 4% 法則 (Trinity Study)
            </div>
        </div>
        <div class="alert-card-neutral" style='flex:1;'>
            <div class="kpi-label">當前退休達標率</div>
            <div style='font-family:"Orbitron",monospace;font-size:1.8rem;
                        color:{"#00ff88" if net_asset >= target_net else "#00d4ff"};margin:8px 0;'>
                {min(net_asset / target_net * 100, 100):.1f}%
            </div>
            <div class="progress-wrap">
                <div class="progress-fill-{'green' if net_asset >= target_net else 'green'}"
                     style='width:{min(net_asset/target_net*100, 100):.1f}%;'></div>
            </div>
            <div style='font-family:"Share Tech Mono",monospace;font-size:0.65rem;color:#5a7a8a;margin-top:6px;'>
                {fmt_twd(net_asset)} / {fmt_twd(target_net)}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ROW 5 — STRATEGY SOP
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
with st.expander("⚙  STRATEGY SOP — 核心操作規則 (點擊展開)"):
    st.markdown("""
    <div style='font-family:"Share Tech Mono",monospace;font-size:0.78rem;
                color:#5a7a8a;line-height:2;padding:8px 4px;'>
    <span style='color:#00d4ff;'>PHASE 1 ›</span>
        每月定期定額買入 <span style='color:#00ff88;'>00631L</span>，持續累積至市值 ≥ 100 萬 TWD<br>
    <span style='color:#00d4ff;'>PHASE 2 ›</span>
        00631L 達標後，全數賣出並轉入 <span style='color:#00ff88;'>006208</span>，建立質押部位<br>
    <span style='color:#00d4ff;'>PHASE 3 ›</span>
        維持 006208 質押率 ≥ 250%，借出資金持續買入 <span style='color:#00ff88;'>2330</span> (台積電)<br>
    <span style='color:#ffaa00;'>RISK MGT ›</span>
        維持率警戒：&lt; 220% 立即補充擔保品或還款；定期追蹤借款到期日
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center;padding:16px 0 8px 0;border-top:1px solid #1e3a4a;'>
    <span style='font-family:"Share Tech Mono",monospace;font-size:0.6rem;color:#2a4a5a;
                 letter-spacing:0.15em;'>
        PROJECT F.I.R.E &nbsp;│&nbsp; BUILD FOR FINANCIAL INDEPENDENCE
        &nbsp;│&nbsp; DATA: YFINANCE · NOT FINANCIAL ADVICE
        &nbsp;│&nbsp; {now_str}
    </span>
</div>
""", unsafe_allow_html=True)
