import streamlit as st
from streamlit_cookies_controller import CookieController
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
# PERSISTENT SETTINGS VIA COOKIES
# ─────────────────────────────────────────────
_cookies = CookieController()

def ck_int(key, default):
    try:
        v = _cookies.get("fire_" + key)
        return int(v) if v is not None else default
    except: return default

def ck_float(key, default):
    try:
        v = _cookies.get("fire_" + key)
        return float(v) if v is not None else default
    except: return default

def ck_date(key, default):
    try:
        v = _cookies.get("fire_" + key)
        return date.fromisoformat(v) if v is not None else default
    except: return default

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
    shares_006208 = st.number_input("006208 持股 (股)", min_value=0, value=ck_int("s1", 10000), step=100, key="s1")
    shares_00631L = st.number_input("00631L 持股 (股)", min_value=0, value=ck_int("s2", 5000),  step=100, key="s2")
    shares_2330   = st.number_input("2330 持股 (股)",   min_value=0, value=ck_int("s3", 200),    step=10,  key="s3")

    st.markdown("### 🏦 質押條件")
    pledge_loan = st.number_input(
        "質押借款總額 (TWD)", min_value=0,
        value=ck_int("pl", 1_500_000), step=10_000,
        help="目前向券商借出的總金額"
    )
    pledge_rate = st.number_input(
        "質押年利率 (%)", min_value=0.0,
        value=ck_float("pr", 2.4), step=0.1, format="%.2f"
    )
    pledge_expiry = st.date_input(
        "借款到期日",
        value=ck_date("pe", date.today() + timedelta(days=180)),
        min_value=date.today(),
    )

    st.markdown("### 🎯 退休目標")
    target_net = st.number_input(
        "目標淨資產 (TWD)", min_value=1_000_000,
        value=ck_int("tn", 30_000_000), step=500_000
    )
    monthly_invest = st.number_input(
        "每月定額投入 (TWD)", min_value=0,
        value=ck_int("mi", 30_000), step=1_000
    )
    withdrawal_rate = st.number_input(
        "安全提領率 (%)", min_value=1.0, max_value=10.0,
        value=ck_float("wr", 4.0), step=0.1, format="%.1f"
    )
    dob = st.date_input(
        "出生年月日",
        value=ck_date("dob", date(1992, 12, 14)),
        min_value=date(1950, 1, 1),
        max_value=date.today() - timedelta(days=365*18),
    )

    st.markdown("---")

    if st.button("💾  儲存設定", use_container_width=True):
        _cookies.set("fire_s1",  str(shares_006208),  max_age=365*24*3600)
        _cookies.set("fire_s2",  str(shares_00631L),   max_age=365*24*3600)
        _cookies.set("fire_s3",  str(shares_2330),     max_age=365*24*3600)
        _cookies.set("fire_pl",  str(int(pledge_loan)), max_age=365*24*3600)
        _cookies.set("fire_pr",  str(pledge_rate),     max_age=365*24*3600)
        _cookies.set("fire_pe",  pledge_expiry.isoformat(), max_age=365*24*3600)
        _cookies.set("fire_tn",  str(int(target_net)), max_age=365*24*3600)
        _cookies.set("fire_mi",  str(int(monthly_invest)), max_age=365*24*3600)
        _cookies.set("fire_wr",  str(withdrawal_rate), max_age=365*24*3600)
        _cookies.set("fire_dob", dob.isoformat(),      max_age=365*24*3600)
        st.success("✅ 設定已儲存！下次開啟自動載入")

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

    ratio_display = f"{pledge_ratio:.1f}" if pledge_loan > 0 else "∞"
    st.markdown(f"""
    <div class="{ratio_class}">
        <div class="kpi-label">006208 質押維持率</div>
        <div class="kpi-num" style='color:{ratio_color};'>
            {ratio_display}<span style='font-size:1rem;'>%</span>
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
# ROW 5 — 季線回測：貸款投資 00631L
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="section-header">[ 05 ]  季線回測 · 00631L 貸款投資評估</div>', unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def fetch_backtest_data(period="5y"):
    try:
        tkr = yf.Ticker("00631L.TW")
        df  = tkr.history(period=period)
        if df.empty:
            return None
        df = df[["Close","Volume"]].copy()
        df.index = pd.to_datetime(df.index).tz_localize(None)
        return df
    except:
        return None

# ── Backtest controls ──
bt_c1, bt_c2, bt_c3, bt_c4 = st.columns(4)
with bt_c1:
    bt_period = st.selectbox("回測期間", ["1y","2y","3y","5y"], index=3, key="bt_period")
with bt_c2:
    bt_capital = st.number_input("初始本金 (TWD)", min_value=10000,
                                  value=ck_int("bt_cap", 300000), step=10000, key="bt_cap_input")
with bt_c3:
    bt_loan = st.number_input("貸款金額 (TWD)", min_value=0,
                               value=ck_int("bt_loan", 700000), step=10000, key="bt_loan_input")
with bt_c4:
    bt_rate = st.number_input("貸款年利率 (%)", min_value=0.0,
                               value=ck_float("bt_rate", float(pledge_rate)),
                               step=0.1, format="%.2f", key="bt_rate_input")

bt_df = fetch_backtest_data(bt_period)

if bt_df is None or len(bt_df) < 65:
    st.markdown("""
    <div class="alert-card-amber">
        <span style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#ffaa00;">
            ⚠ 無法取得 00631L 歷史資料，請稍後再試
        </span>
    </div>""", unsafe_allow_html=True)
else:
    # ── Calculate indicators ──
    df = bt_df.copy()
    df["MA60"]  = df["Close"].rolling(60).mean()   # 季線
    df["MA20"]  = df["Close"].rolling(20).mean()   # 月線
    df["MA120"] = df["Close"].rolling(120).mean()  # 半年線
    df = df.dropna()

    total_invest = bt_capital + bt_loan
    daily_interest_cost = bt_loan * (bt_rate / 100) / 365

    # ── Strategy A: 季線多空策略 with leverage ──
    # Buy when Close > MA60 (above 季線), sell when Close < MA60
    cash_lev     = total_invest
    shares_lev   = 0.0
    equity_lev   = []
    in_market_lev = False

    # ── Strategy B: 純持有（buy & hold）with same capital ──
    shares_hold  = total_invest / df["Close"].iloc[0]
    loan_days    = 0

    trades       = []

    for i, (idx, row) in enumerate(df.iterrows()):
        price  = row["Close"]
        ma60   = row["MA60"]

        above_ma60 = price > ma60

        if above_ma60 and not in_market_lev:
            # BUY signal
            shares_lev    = cash_lev / price
            cash_lev      = 0.0
            in_market_lev = True
            trades.append({"date": idx, "action": "BUY", "price": price, "ma60": ma60})

        elif not above_ma60 and in_market_lev:
            # SELL signal
            cash_lev      = shares_lev * price
            shares_lev    = 0.0
            in_market_lev = False
            trades.append({"date": idx, "action": "SELL", "price": price, "ma60": ma60})

        # Deduct daily interest when holding (leveraged)
        if in_market_lev:
            loan_days += 1
            cash_lev  -= daily_interest_cost  # deduct from equity

        # Track equity
        lev_equity  = (shares_lev * price + cash_lev) - bt_loan
        hold_equity = (shares_hold * price) - bt_loan
        equity_lev.append({
            "date":     idx,
            "price":    price,
            "ma60":     ma60,
            "ma20":     row["MA20"],
            "ma120":    row["MA120"],
            "lev_eq":   lev_equity,
            "hold_eq":  hold_equity,
            "in_mkt":   in_market_lev,
        })

    result_df = pd.DataFrame(equity_lev).set_index("date")

    # Force-close last position
    if in_market_lev:
        final_price    = df["Close"].iloc[-1]
        final_lev_eq   = shares_lev * final_price + cash_lev - bt_loan
    else:
        final_lev_eq   = cash_lev - bt_loan

    # ── Performance metrics ──
    years = len(df) / 252

    # Leveraged strategy
    lev_final   = result_df["lev_eq"].iloc[-1]
    lev_ret     = (lev_final - bt_capital) / bt_capital * 100
    lev_ann     = ((lev_final / bt_capital) ** (1 / years) - 1) * 100 if bt_capital > 0 and lev_final > 0 else 0
    lev_dd_ser  = result_df["lev_eq"]
    lev_peak    = lev_dd_ser.cummax()
    lev_dd      = ((lev_dd_ser - lev_peak) / lev_peak.abs()).min() * 100

    # Buy & Hold
    hold_final  = result_df["hold_eq"].iloc[-1]
    hold_ret    = (hold_final - bt_capital) / bt_capital * 100
    hold_ann    = ((hold_final / bt_capital) ** (1 / years) - 1) * 100 if bt_capital > 0 and hold_final > 0 else 0
    hold_dd_ser = result_df["hold_eq"]
    hold_peak   = hold_dd_ser.cummax()
    hold_dd     = ((hold_dd_ser - hold_peak) / hold_peak.abs()).min() * 100

    # Trade stats
    trade_df    = pd.DataFrame(trades)
    total_interest = loan_days * daily_interest_cost
    n_trades    = len([t for t in trades if t["action"] == "BUY"])

    # Win rate
    wins = 0
    buy_price = None
    for t in trades:
        if t["action"] == "BUY":
            buy_price = t["price"]
        elif t["action"] == "SELL" and buy_price:
            if t["price"] > buy_price:
                wins += 1
    win_rate = (wins / n_trades * 100) if n_trades > 0 else 0

    # ── KPI Cards ──
    st.markdown('<br>', unsafe_allow_html=True)
    k1, k2, k3, k4, k5, k6 = st.columns(6)

    def kpi_card(label, value, sub="", color="#00d4ff"):
        return f"""
        <div class="alert-card-neutral" style="text-align:center;padding:12px;">
            <div class="kpi-label">{label}</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:1.15rem;
                        color:{color};font-weight:700;">{value}</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:0.62rem;
                        color:#5a7a8a;margin-top:3px;">{sub}</div>
        </div>"""

    lev_color  = "#00ff88" if lev_ret >= 0 else "#ff3366"
    hold_color = "#00ff88" if hold_ret >= 0 else "#ff3366"

    with k1:
        st.markdown(kpi_card("策略總報酬", f"{lev_ret:+.1f}%",
                             f"年化 {lev_ann:.1f}%", lev_color), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_card("持有總報酬", f"{hold_ret:+.1f}%",
                             f"年化 {hold_ann:.1f}%", hold_color), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_card("策略最大回撤", f"{lev_dd:.1f}%",
                             "季線策略", "#ffaa00"), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi_card("持有最大回撤", f"{hold_dd:.1f}%",
                             "純持有", "#ffaa00"), unsafe_allow_html=True)
    with k5:
        st.markdown(kpi_card("交易次數", f"{n_trades} 次",
                             f"勝率 {win_rate:.0f}%", "#00d4ff"), unsafe_allow_html=True)
    with k6:
        st.markdown(kpi_card("利息成本", fmt_twd(total_interest),
                             f"{loan_days} 天持倉", "#ff3366"), unsafe_allow_html=True)

    # ── Chart ──
    st.markdown('<br>', unsafe_allow_html=True)

    import json

    dates_str     = [d.strftime("%Y-%m-%d") for d in result_df.index]
    price_vals    = result_df["price"].tolist()
    ma60_vals     = result_df["ma60"].tolist()
    ma20_vals     = result_df["ma20"].tolist()
    ma120_vals    = result_df["ma120"].tolist()
    lev_eq_vals   = result_df["lev_eq"].tolist()
    hold_eq_vals  = result_df["hold_eq"].tolist()
    in_mkt_vals   = result_df["in_mkt"].tolist()

    # Build buy/sell markers
    buy_dates  = [t["date"].strftime("%Y-%m-%d") for t in trades if t["action"] == "BUY"]
    buy_prices = [t["price"] for t in trades if t["action"] == "BUY"]
    sell_dates  = [t["date"].strftime("%Y-%m-%d") for t in trades if t["action"] == "SELL"]
    sell_prices = [t["price"] for t in trades if t["action"] == "SELL"]

    chart_html = f"""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
  body {{ background: #080c10; margin: 0; padding: 10px; font-family: 'Share Tech Mono', monospace; }}
  .tab-bar {{ display:flex; gap:8px; margin-bottom:12px; }}
  .tab {{ background:#111820; border:1px solid #1e3a4a; color:#5a7a8a;
          padding:6px 16px; border-radius:4px; cursor:pointer;
          font-size:0.7rem; letter-spacing:0.1em; }}
  .tab.active {{ border-color:#00d4ff; color:#00d4ff; background:rgba(0,212,255,0.05); }}
  .chart-wrap {{ position:relative; height:340px; }}
  .legend {{ display:flex; gap:16px; flex-wrap:wrap; margin-top:8px; }}
  .leg-item {{ display:flex; align-items:center; gap:6px;
               font-size:0.65rem; color:#5a7a8a; letter-spacing:0.05em; }}
  .leg-dot {{ width:10px; height:10px; border-radius:50%; }}
</style>
</head>
<body>
<div class="tab-bar">
  <div class="tab active" onclick="showChart('price')" id="tab-price">價格 & 季線</div>
  <div class="tab" onclick="showChart('equity')" id="tab-equity">淨值曲線比較</div>
</div>

<div class="chart-wrap" id="wrap-price"><canvas id="chartPrice"></canvas></div>
<div class="chart-wrap" id="wrap-equity" style="display:none"><canvas id="chartEquity"></canvas></div>

<div class="legend">
  <div class="leg-item"><div class="leg-dot" style="background:#00d4ff"></div>收盤價</div>
  <div class="leg-item"><div class="leg-dot" style="background:#ffaa00"></div>季線(MA60)</div>
  <div class="leg-item"><div class="leg-dot" style="background:#aaaaff"></div>月線(MA20)</div>
  <div class="leg-item"><div class="leg-dot" style="background:#ff8866"></div>半年線(MA120)</div>
  <div class="leg-item"><div class="leg-dot" style="background:#00ff88"></div>▲ 買入訊號</div>
  <div class="leg-item"><div class="leg-dot" style="background:#ff3366"></div>▼ 賣出訊號</div>
</div>

<script>
const dates    = {json.dumps(dates_str)};
const prices   = {json.dumps([round(x,2) for x in price_vals])};
const ma60     = {json.dumps([round(x,2) for x in ma60_vals])};
const ma20     = {json.dumps([round(x,2) for x in ma20_vals])};
const ma120    = {json.dumps([round(x,2) for x in ma120_vals])};
const levEq    = {json.dumps([round(x,0) for x in lev_eq_vals])};
const holdEq   = {json.dumps([round(x,0) for x in hold_eq_vals])};
const buyDates = {json.dumps(buy_dates)};
const buyPrices= {json.dumps([round(x,2) for x in buy_prices])};
const sellDates= {json.dumps(sell_dates)};
const sellPrices={json.dumps([round(x,2) for x in sell_prices])};

// Buy/Sell scatter data aligned to date index
const buyScatter  = buyDates.map((d,i)  => ({{x: d, y: buyPrices[i]}}));
const sellScatter = sellDates.map((d,i) => ({{x: d, y: sellPrices[i]}}));

const gridColor  = 'rgba(30,58,74,0.6)';
const tickColor  = '#2a4a5a';

const commonScales = {{
  x: {{
    type: 'category',
    ticks: {{ color: tickColor, maxTicksLimit: 8, font:{{size:10}} }},
    grid: {{ color: gridColor }}
  }},
  y: {{
    ticks: {{ color: tickColor, font:{{size:10}} }},
    grid: {{ color: gridColor }}
  }}
}};

// ── Price Chart ──
const ctxP = document.getElementById('chartPrice').getContext('2d');
const priceChart = new Chart(ctxP, {{
  type: 'line',
  data: {{
    labels: dates,
    datasets: [
      {{ label:'收盤價', data: prices, borderColor:'#00d4ff', borderWidth:1.5,
         pointRadius:0, tension:0.1, yAxisID:'yp' }},
      {{ label:'季線MA60', data: ma60,   borderColor:'#ffaa00', borderWidth:2,
         pointRadius:0, tension:0.3, borderDash:[4,2], yAxisID:'yp' }},
      {{ label:'月線MA20', data: ma20,   borderColor:'#aaaaff', borderWidth:1,
         pointRadius:0, tension:0.3, borderDash:[2,3], yAxisID:'yp' }},
      {{ label:'半年線MA120', data: ma120, borderColor:'#ff8866', borderWidth:1,
         pointRadius:0, tension:0.3, borderDash:[6,3], yAxisID:'yp' }},
      {{ label:'買入', data: buyScatter, type:'scatter',
         backgroundColor:'#00ff88', pointRadius:7, pointStyle:'triangle',
         yAxisID:'yp', showLine:false }},
      {{ label:'賣出', data: sellScatter, type:'scatter',
         backgroundColor:'#ff3366', pointRadius:7, pointStyle:'triangle',
         rotation:180, yAxisID:'yp', showLine:false }},
    ]
  }},
  options: {{
    responsive:true, maintainAspectRatio:false,
    plugins:{{ legend:{{display:false}}, tooltip:{{
      mode:'index', intersect:false,
      backgroundColor:'#111820', borderColor:'#1e3a4a', borderWidth:1,
      titleColor:'#00d4ff', bodyColor:'#5a7a8a', titleFont:{{size:11}}
    }}}},
    scales:{{ ...commonScales, yp:{{ position:'left',
      ticks:{{color:tickColor, font:{{size:10}}}}, grid:{{color:gridColor}} }} }}
  }}
}});

// ── Equity Chart ──
const ctxE = document.getElementById('chartEquity').getContext('2d');
const equityChart = new Chart(ctxE, {{
  type: 'line',
  data: {{
    labels: dates,
    datasets: [
      {{ label:'季線策略淨值', data: levEq,  borderColor:'#00ff88', borderWidth:2,
         pointRadius:0, tension:0.1, fill:false }},
      {{ label:'純持有淨值',   data: holdEq, borderColor:'#00d4ff', borderWidth:1.5,
         pointRadius:0, tension:0.1, borderDash:[4,2], fill:false }},
      {{ label:'本金基準線',   data: dates.map(()=>{bt_capital}), borderColor:'#2a4a5a',
         borderWidth:1, pointRadius:0, borderDash:[2,4], fill:false }},
    ]
  }},
  options: {{
    responsive:true, maintainAspectRatio:false,
    plugins:{{ legend:{{ labels:{{ color:'#5a7a8a', font:{{size:10}}, boxWidth:12 }} }},
      tooltip:{{
        mode:'index', intersect:false,
        backgroundColor:'#111820', borderColor:'#1e3a4a', borderWidth:1,
        titleColor:'#00d4ff', bodyColor:'#5a7a8a',
        callbacks:{{ label: ctx => ` ${{ctx.dataset.label}}: ${{ctx.raw.toLocaleString()}}` }}
      }} }},
    scales: commonScales
  }}
}});

function showChart(name) {{
  document.getElementById('wrap-price').style.display  = name==='price'  ? '' : 'none';
  document.getElementById('wrap-equity').style.display = name==='equity' ? '' : 'none';
  document.getElementById('tab-price').classList.toggle('active',  name==='price');
  document.getElementById('tab-equity').classList.toggle('active', name==='equity');
}}
</script>
</body>
</html>"""

    st.components.v1.html(chart_html, height=440, scrolling=False)

    # ── Summary Box ──
    alpha = lev_ret - hold_ret
    alpha_color = "#00ff88" if alpha >= 0 else "#ff3366"
    conclusion = "✅ 季線策略優於純持有" if alpha >= 0 else "⚠ 此期間純持有表現較佳"

    st.markdown(f"""
    <div class="alert-card-neutral" style="margin-top:12px;">
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;">
            <div>
                <div class="kpi-label">超額報酬 (Alpha)</div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:1.2rem;
                            color:{alpha_color};">{alpha:+.1f}%</div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;
                            color:#5a7a8a;">策略 vs 純持有</div>
            </div>
            <div>
                <div class="kpi-label">利息成本 / 總報酬</div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:1.2rem;color:#ffaa00;">
                    {(total_interest / max(abs(lev_final - bt_capital), 1) * 100):.1f}%
                </div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#5a7a8a;">
                    利息侵蝕比例
                </div>
            </div>
            <div>
                <div class="kpi-label">回測結論</div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:0.85rem;
                            color:{alpha_color};line-height:1.4;">{conclusion}</div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#5a7a8a;">
                    {bt_period} 回測 · 季線進出場
                </div>
            </div>
        </div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:#2a4a5a;
                    margin-top:12px;line-height:1.8;">
            策略邏輯：收盤價 > 季線(MA60) → 全倉買入 ｜ 收盤價 < 季線 → 全數賣出<br>
            資金結構：本金 {fmt_twd(bt_capital)} + 貸款 {fmt_twd(bt_loan)} = 總資金 {fmt_twd(total_invest)}<br>
            利率成本：年利率 {bt_rate:.2f}% · 實際持倉 {loan_days} 天 · 總利息 {fmt_twd(total_interest)}<br>
            ⚠ 以上為歷史回測，不代表未來績效，貸款投資有強制平倉風險
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
