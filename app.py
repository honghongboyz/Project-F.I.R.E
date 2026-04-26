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
# PERSISTENT SETTINGS — localStorage via JS bridge
# ─────────────────────────────────────────────

# JS component: on load, read localStorage and push into query params via redirect
st.components.v1.html("""
<script>
(function(){
  var KEYS = ["s1","s2","s3","pl","pr","pe","tn","mi","wr","dob"];
  try {
    var store = window.parent.localStorage;
    // Check if current URL already has our params (just saved)
    var urlParams = new URLSearchParams(window.parent.location.search);
    var hasParams = KEYS.every(function(k){ return urlParams.has(k); });
    if (hasParams) {
      // Save fresh values from URL into localStorage
      KEYS.forEach(function(k){
        store.setItem("fire_"+k, urlParams.get(k));
      });
      return;
    }
    // Otherwise: load from localStorage into URL and redirect
    var stored = {};
    var allFound = true;
    KEYS.forEach(function(k){
      var v = store.getItem("fire_"+k);
      if (v !== null) { stored[k] = v; } else { allFound = false; }
    });
    if (allFound) {
      var url = new URL(window.parent.location.href);
      KEYS.forEach(function(k){ url.searchParams.set(k, stored[k]); });
      window.parent.location.replace(url.toString());
    }
  } catch(e) { console.log("storage error:", e); }
})();
</script>
""", height=0)

def ck_int(key, default):
    try:    return int(st.query_params[key])
    except: return default

def ck_float(key, default):
    try:    return float(st.query_params[key])
    except: return default

def ck_date(key, default):
    try:    return date.fromisoformat(st.query_params[key])
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

    # ── Auto-sync settings to URL query params every render ──
    _params = {
        "s1":  str(shares_006208),
        "s2":  str(shares_00631L),
        "s3":  str(shares_2330),
        "pl":  str(int(pledge_loan)),
        "pr":  str(pledge_rate),
        "pe":  pledge_expiry.isoformat(),
        "tn":  str(int(target_net)),
        "mi":  str(int(monthly_invest)),
        "wr":  str(withdrawal_rate),
        "dob": dob.isoformat(),
    }
    st.query_params.update(_params)

    # ── JS: auto-write to localStorage on every render ──
    import json as _json
    _js_vals = _json.dumps(_params)
    st.components.v1.html(f"""
    <script>
    (function(){{
      try {{
        var data = {_js_vals};
        var store = window.parent.localStorage;
        Object.keys(data).forEach(function(k){{
          store.setItem("fire_"+k, data[k]);
        }});
      }} catch(e) {{ console.log("save error:", e); }}
    }})();
    </script>
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;
                color:#1a3a2a;text-align:center;padding:4px 0;letter-spacing:0.08em;">
        ✓ 設定自動記憶中
    </div>
    """, height=22)

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

# ─────────────────────────────────────────────
# DATA PERSISTENCE — localStorage JSON bridge
# ─────────────────────────────────────────────
import json as _json
import base64 as _b64

def _encode(obj): return _b64.b64encode(_json.dumps(obj, ensure_ascii=False).encode()).decode()
def _decode(s, default):
    try: return _json.loads(_b64.b64decode(s).decode())
    except: return default

# Load persisted data from query params (written by JS on prev session)
_raw_snap  = st.query_params.get("snap",  "")
_raw_dca   = st.query_params.get("dca",   "")
_raw_fun   = st.query_params.get("fun",   "")
_raw_big   = st.query_params.get("big",   "")
_raw_fcfg  = st.query_params.get("fcfg",  "")

if "snapshots"   not in st.session_state: st.session_state.snapshots   = _decode(_raw_snap, [])
if "dca_records" not in st.session_state: st.session_state.dca_records = _decode(_raw_dca,  [])
if "fun_exp"     not in st.session_state: st.session_state.fun_exp     = _decode(_raw_fun,  [])
if "big_plans"   not in st.session_state: st.session_state.big_plans   = _decode(_raw_big,  [])
if "fun_budget"  not in st.session_state:
    cfg = _decode(_raw_fcfg, {})
    st.session_state.fun_budget = cfg.get("budget", 5000)

def _persist():
    """Write all app data into URL query params (JS will auto-save to localStorage)."""
    st.query_params.update({
        "snap": _encode(st.session_state.snapshots),
        "dca":  _encode(st.session_state.dca_records),
        "fun":  _encode(st.session_state.fun_exp),
        "big":  _encode(st.session_state.big_plans),
        "fcfg": _encode({"budget": st.session_state.fun_budget}),
    })

# ─────────────────────────────────────────────
# ROW 5 — 月報快照 MONTHLY SNAPSHOT
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="section-header">[ 05 ]  月報快照 · MONTHLY NET ASSET SNAPSHOT</div>', unsafe_allow_html=True)

snap_c1, snap_c2 = st.columns([2, 3])

with snap_c1:
    st.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#5a7a8a;margin-bottom:8px;letter-spacing:0.08em;">記錄本月淨資產</div>', unsafe_allow_html=True)
    snap_note = st.text_input("備註 (可留空)", placeholder="e.g. 加薪、買新股", key="snap_note", label_visibility="collapsed")
    if st.button("📸  記錄本月快照", use_container_width=True):
        entry = {
            "date":  datetime.now().strftime("%Y-%m"),
            "net":   round(net_asset),
            "total": round(total_mv),
            "note":  snap_note or "",
        }
        # Avoid duplicate same month
        st.session_state.snapshots = [s for s in st.session_state.snapshots if s["date"] != entry["date"]]
        st.session_state.snapshots.append(entry)
        st.session_state.snapshots.sort(key=lambda x: x["date"])
        _persist()
        st.success(f"✅ {entry['date']} 快照已儲存")

    if st.session_state.snapshots:
        if st.button("🗑  刪除最後一筆", use_container_width=True):
            st.session_state.snapshots.pop()
            _persist()
            st.rerun()

with snap_c2:
    if len(st.session_state.snapshots) >= 2:
        snaps = st.session_state.snapshots
        labels_js = _json.dumps([s["date"] for s in snaps])
        net_js    = _json.dumps([s["net"]   for s in snaps])
        total_js  = _json.dumps([s["total"] for s in snaps])

        # Growth stats
        first_net = snaps[0]["net"]; last_net = snaps[-1]["net"]
        growth    = last_net - first_net
        growth_pct = (growth / abs(first_net) * 100) if first_net != 0 else 0
        months_cnt = len(snaps)
        monthly_avg = growth / max(months_cnt - 1, 1)

        g_col = "#00ff88" if growth >= 0 else "#ff3366"

        snap_html = f"""<!DOCTYPE html><html><body style="margin:0;background:transparent;">
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:10px;">
  <div style="background:#0d1117;border:1px solid #1e3a4a;border-radius:6px;padding:10px;">
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.58rem;color:#5a7a8a;letter-spacing:0.1em;">累計成長</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:1rem;color:{g_col};">{'+ ' if growth>=0 else ''}{growth/10000:.1f}萬</div>
  </div>
  <div style="background:#0d1117;border:1px solid #1e3a4a;border-radius:6px;padding:10px;">
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.58rem;color:#5a7a8a;letter-spacing:0.1em;">成長率</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:1rem;color:{g_col};">{growth_pct:+.1f}%</div>
  </div>
  <div style="background:#0d1117;border:1px solid #1e3a4a;border-radius:6px;padding:10px;">
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.58rem;color:#5a7a8a;letter-spacing:0.1em;">月均增加</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:1rem;color:#00d4ff;">{monthly_avg/10000:+.1f}萬</div>
  </div>
</div>
<canvas id="snapChart" height="130"></canvas>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<script>
var ctx = document.getElementById('snapChart').getContext('2d');
new Chart(ctx, {{
  type: 'line',
  data: {{
    labels: {labels_js},
    datasets: [
      {{label:'淨資產', data:{net_js}, borderColor:'#00ff88', backgroundColor:'rgba(0,255,136,0.08)',
       borderWidth:2, pointBackgroundColor:'#00ff88', pointRadius:4, fill:true, tension:0.3}},
      {{label:'總市值', data:{total_js}, borderColor:'#00d4ff', borderWidth:1.5,
       borderDash:[4,4], pointRadius:2, fill:false, tension:0.3}}
    ]
  }},
  options: {{
    responsive:true, animation:false,
    plugins:{{legend:{{labels:{{color:'#5a7a8a',font:{{size:10,family:'Share Tech Mono'}}}}}} }},
    scales:{{
      x:{{ticks:{{color:'#5a7a8a',font:{{size:9}}}}, grid:{{color:'#1e3a4a'}}}},
      y:{{ticks:{{color:'#5a7a8a',font:{{size:9}},
           callback:function(v){{return (v/10000).toFixed(0)+'萬';}}}},
         grid:{{color:'#1e3a4a'}}}}
    }}
  }}
}});
</script></body></html>"""
        st.components.v1.html(snap_html, height=220)
    elif len(st.session_state.snapshots) == 1:
        s = st.session_state.snapshots[0]
        st.markdown(f"""<div class="alert-card-neutral" style="text-align:center;padding:20px;">
        <div style="font-family:'Share Tech Mono',monospace;color:#5a7a8a;font-size:0.75rem;">
            已記錄 {s['date']} 淨資產 {s['net']/10000:.1f}萬<br>再記錄一個月即可看到成長曲線 📈
        </div></div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-card-neutral" style="text-align:center;padding:24px;"><div style="font-family:Share Tech Mono,monospace;color:#5a7a8a;font-size:0.75rem;">尚無快照資料<br>按左側按鈕記錄本月淨資產</div></div>', unsafe_allow_html=True)

# Show snapshot table
if st.session_state.snapshots:
    with st.expander(f"📋  查看所有快照記錄（共 {len(st.session_state.snapshots)} 筆）"):
        rows = ""
        for i, s in enumerate(reversed(st.session_state.snapshots)):
            rows += f"""<tr style="border-bottom:1px solid #1a2a3a;">
              <td style="padding:8px 12px;font-family:'Share Tech Mono',monospace;color:#00d4ff;font-size:0.8rem;">{s['date']}</td>
              <td style="padding:8px 12px;font-family:'Share Tech Mono',monospace;color:#00ff88;font-size:0.8rem;">{s['net']/10000:.2f} 萬</td>
              <td style="padding:8px 12px;font-family:'Share Tech Mono',monospace;color:#5a7a8a;font-size:0.75rem;">{s['total']/10000:.2f} 萬</td>
              <td style="padding:8px 12px;font-family:'Share Tech Mono',monospace;color:#5a7a8a;font-size:0.75rem;">{s.get('note','')}</td>
            </tr>"""
        st.markdown(f"""<div class="alert-card-neutral" style="overflow-x:auto;">
          <table style="width:100%;border-collapse:collapse;">
            <thead><tr style="border-bottom:2px solid #1e3a4a;">
              <th style="padding:8px 12px;font-family:'Share Tech Mono',monospace;font-size:0.62rem;color:#5a7a8a;text-align:left;">月份</th>
              <th style="padding:8px 12px;font-family:'Share Tech Mono',monospace;font-size:0.62rem;color:#5a7a8a;text-align:left;">淨資產</th>
              <th style="padding:8px 12px;font-family:'Share Tech Mono',monospace;font-size:0.62rem;color:#5a7a8a;text-align:left;">總市值</th>
              <th style="padding:8px 12px;font-family:'Share Tech Mono',monospace;font-size:0.62rem;color:#5a7a8a;text-align:left;">備註</th>
            </tr></thead>
            <tbody>{rows}</tbody>
          </table></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 6 — 00631L 定期定額追蹤器
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="section-header">[ 06 ]  定期定額追蹤器 · 00631L DCA TRACKER</div>', unsafe_allow_html=True)

dca_c1, dca_c2 = st.columns([2, 3])

with dca_c1:
    st.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#5a7a8a;margin-bottom:8px;letter-spacing:0.08em;">新增買入記錄</div>', unsafe_allow_html=True)
    dca_date   = st.date_input("買入日期", value=date.today(), key="dca_date")
    dca_shares = st.number_input("買入股數", min_value=1, value=1000, step=100, key="dca_shares")
    dca_price  = st.number_input("買入價格 (TWD)", min_value=0.1, value=float(p_00631L) if p_00631L else 27.0, step=0.1, format="%.2f", key="dca_price")

    if st.button("➕  新增買入記錄", use_container_width=True):
        st.session_state.dca_records.append({
            "date":   str(dca_date),
            "shares": dca_shares,
            "price":  round(dca_price, 2),
            "cost":   round(dca_shares * dca_price),
        })
        st.session_state.dca_records.sort(key=lambda x: x["date"])
        _persist()
        st.success("✅ 已新增")

    if st.session_state.dca_records:
        if st.button("🗑  刪除最後一筆", use_container_width=True, key="dca_del"):
            st.session_state.dca_records.pop()
            _persist()
            st.rerun()

with dca_c2:
    if st.session_state.dca_records:
        records = st.session_state.dca_records
        total_shares = sum(r["shares"] for r in records)
        total_cost   = sum(r["cost"]   for r in records)
        avg_price    = total_cost / total_shares if total_shares > 0 else 0
        current_val  = total_shares * p_00631L if p_00631L else 0
        pnl          = current_val - total_cost
        pnl_pct      = pnl / total_cost * 100 if total_cost > 0 else 0
        pnl_col      = "#00ff88" if pnl >= 0 else "#ff3366"
        target_gap   = 1_000_000 - current_val
        target_pct   = min(current_val / 1_000_000 * 100, 100)

        st.markdown(f"""
        <div class="alert-card-neutral">
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px;">
            <div>
              <div class="kpi-label">平均成本</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:1.1rem;color:#00d4ff;">${avg_price:.2f}</div>
              <div class="kpi-sub">現價 ${p_00631L:.2f if p_00631L else '--'}</div>
            </div>
            <div>
              <div class="kpi-label">未實現損益</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:1.1rem;color:{pnl_col};">{pnl:+,.0f}</div>
              <div class="kpi-sub" style="color:{pnl_col};">{pnl_pct:+.2f}%</div>
            </div>
            <div>
              <div class="kpi-label">總持股</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:1.1rem;color:#e8f4f8;">{total_shares:,} 股</div>
              <div class="kpi-sub">市值 ${current_val:,.0f}</div>
            </div>
          </div>
          <div class="kpi-label" style="margin-bottom:4px;">100萬目標進度</div>
          <div class="progress-wrap">
            <div class="progress-fill-{'green' if target_pct >= 100 else 'amber'}" style="width:{target_pct:.1f}%;"></div>
          </div>
          <div style="display:flex;justify-content:space-between;">
            <span style="font-family:'Share Tech Mono',monospace;font-size:0.68rem;color:#5a7a8a;">{target_pct:.1f}% 達成</span>
            <span style="font-family:'Share Tech Mono',monospace;font-size:0.68rem;color:#ffaa00;">
              {'🎯 達標！可執行轉換' if target_gap <= 0 else f'尚差 ${max(target_gap,0):,.0f}'}
            </span>
          </div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#2a4a5a;margin-top:8px;">
            共 {len(records)} 筆買入 · 總成本 ${total_cost:,.0f}
          </div>
        </div>""", unsafe_allow_html=True)

        # DCA table
        with st.expander(f"📋  查看所有買入記錄（{len(records)} 筆）"):
            rows = ""
            for r in reversed(records):
                cost_per = r["cost"]
                curr_val = r["shares"] * (p_00631L or 0)
                r_pnl    = curr_val - cost_per
                r_col    = "#00ff88" if r_pnl >= 0 else "#ff3366"
                rows += f"""<tr style="border-bottom:1px solid #1a2a3a;">
                  <td style="padding:8px 12px;font-family:'Share Tech Mono',monospace;color:#00d4ff;font-size:0.78rem;">{r['date']}</td>
                  <td style="padding:8px 12px;font-family:'Share Tech Mono',monospace;color:#e8f4f8;font-size:0.78rem;">{r['shares']:,}</td>
                  <td style="padding:8px 12px;font-family:'Share Tech Mono',monospace;color:#e8f4f8;font-size:0.78rem;">${r['price']:.2f}</td>
                  <td style="padding:8px 12px;font-family:'Share Tech Mono',monospace;color:#5a7a8a;font-size:0.78rem;">${cost_per:,.0f}</td>
                  <td style="padding:8px 12px;font-family:'Share Tech Mono',monospace;color:{r_col};font-size:0.78rem;">{r_pnl:+,.0f}</td>
                </tr>"""
            st.markdown(f"""<div class="alert-card-neutral" style="overflow-x:auto;">
              <table style="width:100%;border-collapse:collapse;">
                <thead><tr style="border-bottom:2px solid #1e3a4a;">
                  <th style="padding:8px 12px;font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:#5a7a8a;text-align:left;">日期</th>
                  <th style="padding:8px 12px;font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:#5a7a8a;text-align:left;">股數</th>
                  <th style="padding:8px 12px;font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:#5a7a8a;text-align:left;">買入價</th>
                  <th style="padding:8px 12px;font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:#5a7a8a;text-align:left;">成本</th>
                  <th style="padding:8px 12px;font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:#5a7a8a;text-align:left;">損益</th>
                </tr></thead>
                <tbody>{rows}</tbody>
              </table></div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-card-neutral" style="text-align:center;padding:24px;"><div style="font-family:Share Tech Mono,monospace;color:#5a7a8a;font-size:0.75rem;">尚無定額買入記錄<br>從左側新增第一筆</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 7 — 娛樂基金罐子
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="section-header">[ 07 ]  娛樂基金罐子 · FUN FUND JAR</div>', unsafe_allow_html=True)

fun_c1, fun_c2 = st.columns([2, 3])
cur_month_str = datetime.now().strftime("%Y-%m")
this_month_exp = [e for e in st.session_state.fun_exp if e.get("month") == cur_month_str]
spent_this_month = sum(e["amount"] for e in this_month_exp)

with fun_c1:
    new_budget = st.number_input("每月娛樂預算 (TWD)", min_value=0, value=st.session_state.fun_budget, step=500, key="fun_budget_input")
    if new_budget != st.session_state.fun_budget:
        st.session_state.fun_budget = new_budget
        _persist()

    fun_amount = st.number_input("花費金額", min_value=1, value=500, step=100, key="fun_amt")
    fun_label  = st.text_input("花在哪裡？", placeholder="e.g. 電影、聚餐、遊戲", key="fun_label")

    if st.button("💸  記錄花費", use_container_width=True):
        st.session_state.fun_exp.append({
            "month":  cur_month_str,
            "date":   datetime.now().strftime("%Y-%m-%d"),
            "amount": fun_amount,
            "label":  fun_label or "未分類",
        })
        _persist()
        st.success(f"✅ 已記錄 ${fun_amount:,}")

    if this_month_exp:
        if st.button("🗑  刪除本月最後一筆", use_container_width=True, key="fun_del"):
            # Remove last entry from this month
            for i in range(len(st.session_state.fun_exp)-1, -1, -1):
                if st.session_state.fun_exp[i].get("month") == cur_month_str:
                    st.session_state.fun_exp.pop(i)
                    break
            _persist()
            st.rerun()

with fun_c2:
    budget = st.session_state.fun_budget
    remaining = budget - spent_this_month
    used_pct  = min(spent_this_month / budget * 100, 100) if budget > 0 else 0
    rem_col   = "#00ff88" if remaining >= 0 else "#ff3366"
    bar_class = "progress-fill-green" if used_pct < 70 else ("progress-fill-amber" if used_pct < 100 else "progress-fill-red")
    days_in_month = 31
    today_day = datetime.now().day
    daily_budget = remaining / max(days_in_month - today_day, 1) if remaining > 0 else 0

    st.markdown(f"""
    <div class="alert-card-neutral">
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#5a7a8a;
                  letter-spacing:0.1em;margin-bottom:8px;">{cur_month_str} 娛樂預算</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px;">
        <div>
          <div class="kpi-label">已花費</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:1.1rem;color:#ffaa00;">${spent_this_month:,.0f}</div>
          <div class="kpi-sub">{used_pct:.1f}% 預算</div>
        </div>
        <div>
          <div class="kpi-label">剩餘可花</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:1.1rem;color:{rem_col};">${remaining:,.0f}</div>
          <div class="kpi-sub">{'✅ 預算內' if remaining >= 0 else '⚠ 超支'}</div>
        </div>
        <div>
          <div class="kpi-label">每日剩餘額度</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:1.1rem;color:#00d4ff;">${daily_budget:,.0f}</div>
          <div class="kpi-sub">剩 {days_in_month - today_day} 天</div>
        </div>
      </div>
      <div class="kpi-label">本月使用進度</div>
      <div class="progress-wrap">
        <div class="{bar_class}" style="width:{used_pct:.1f}%;"></div>
      </div>
      <div style="display:flex;justify-content:space-between;margin-top:4px;">
        <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#5a7a8a;">${spent_this_month:,.0f} 已花</span>
        <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#5a7a8a;">預算 ${budget:,.0f}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    if this_month_exp:
        with st.expander(f"📋  本月花費明細（{len(this_month_exp)} 筆）"):
            rows = ""
            for e in reversed(this_month_exp):
                rows += f"""<tr style="border-bottom:1px solid #1a2a3a;">
                  <td style="padding:7px 12px;font-family:'Share Tech Mono',monospace;color:#5a7a8a;font-size:0.78rem;">{e['date']}</td>
                  <td style="padding:7px 12px;font-family:'Share Tech Mono',monospace;color:#e8f4f8;font-size:0.78rem;">{e['label']}</td>
                  <td style="padding:7px 12px;font-family:'Share Tech Mono',monospace;color:#ffaa00;font-size:0.78rem;">${e['amount']:,}</td>
                </tr>"""
            st.markdown(f"""<div class="alert-card-neutral" style="overflow-x:auto;">
              <table style="width:100%;border-collapse:collapse;">
                <thead><tr style="border-bottom:2px solid #1e3a4a;">
                  <th style="padding:7px 12px;font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:#5a7a8a;text-align:left;">日期</th>
                  <th style="padding:7px 12px;font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:#5a7a8a;text-align:left;">項目</th>
                  <th style="padding:7px 12px;font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:#5a7a8a;text-align:left;">金額</th>
                </tr></thead>
                <tbody>{rows}</tbody>
              </table></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 8 — 大額支出預存計畫
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="section-header">[ 08 ]  大額支出預存計畫 · BIG EXPENSE PLANNER</div>', unsafe_allow_html=True)

big_c1, big_c2 = st.columns([2, 3])

with big_c1:
    st.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#5a7a8a;margin-bottom:8px;letter-spacing:0.08em;">新增預存計畫</div>', unsafe_allow_html=True)
    big_name   = st.text_input("計畫名稱", placeholder="e.g. 日本旅遊、新電腦", key="big_name")
    big_target = st.number_input("目標金額 (TWD)", min_value=100, value=50000, step=1000, key="big_target")
    big_date   = st.date_input("預計花費日期", value=date.today() + timedelta(days=180), key="big_date")
    big_saved  = st.number_input("已存金額 (TWD)", min_value=0, value=0, step=1000, key="big_saved")

    if st.button("➕  新增計畫", use_container_width=True):
        if big_name:
            st.session_state.big_plans.append({
                "name":    big_name,
                "target":  big_target,
                "date":    str(big_date),
                "saved":   big_saved,
            })
            _persist()
            st.success(f"✅ {big_name} 計畫已新增")
        else:
            st.warning("請輸入計畫名稱")

with big_c2:
    if st.session_state.big_plans:
        for idx, plan in enumerate(st.session_state.big_plans):
            target    = plan["target"]
            saved     = plan["saved"]
            remaining = target - saved
            days_left = (date.fromisoformat(plan["date"]) - date.today()).days
            months_left = max(days_left / 30.44, 0.1)
            monthly_need = remaining / months_left if remaining > 0 else 0
            pct  = min(saved / target * 100, 100) if target > 0 else 0
            pct_col  = "#00ff88" if pct >= 100 else ("#ffaa00" if pct >= 50 else "#00d4ff")
            bar_cls  = "progress-fill-green" if pct >= 100 else ("progress-fill-amber" if pct >= 50 else "progress-fill-green")
            urgent   = days_left < 30
            urg_col  = "#ff3366" if urgent else "#5a7a8a"

            card_html = f"""
            <div class="alert-card-neutral" style="margin-bottom:10px;">
              <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px;">
                <span style="font-family:'Orbitron',monospace;font-size:0.85rem;color:#00d4ff;">{plan['name']}</span>
                <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:{urg_col};">
                  {'🔴 ' if urgent else ''}剩 {days_left} 天
                </span>
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;margin-bottom:10px;">
                <div>
                  <div class="kpi-label">目標</div>
                  <div style="font-family:'Share Tech Mono',monospace;font-size:0.9rem;color:#e8f4f8;">${target:,}</div>
                </div>
                <div>
                  <div class="kpi-label">已存</div>
                  <div style="font-family:'Share Tech Mono',monospace;font-size:0.9rem;color:#00ff88;">${saved:,}</div>
                </div>
                <div>
                  <div class="kpi-label">缺口</div>
                  <div style="font-family:'Share Tech Mono',monospace;font-size:0.9rem;color:#ffaa00;">${remaining:,}</div>
                </div>
                <div>
                  <div class="kpi-label">每月需存</div>
                  <div style="font-family:'Share Tech Mono',monospace;font-size:0.9rem;color:#ff3366;">${monthly_need:,.0f}</div>
                </div>
              </div>
              <div class="progress-wrap">
                <div class="{bar_cls}" style="width:{pct:.1f}%;"></div>
              </div>
              <div style="display:flex;justify-content:space-between;margin-top:4px;">
                <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:{pct_col};">{pct:.1f}% 完成</span>
                <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#5a7a8a;">{plan['date']}</span>
              </div>
            </div>"""
            st.markdown(card_html, unsafe_allow_html=True)

            bc1, bc2, bc3 = st.columns([2, 2, 1])
            with bc1:
                add_amt = st.number_input(f"追加存入 #{idx+1}", min_value=0, value=0, step=500, key=f"add_{idx}", label_visibility="collapsed")
            with bc2:
                if st.button(f"💰 追加存入 #{idx+1}", key=f"addbtn_{idx}", use_container_width=True):
                    if add_amt > 0:
                        st.session_state.big_plans[idx]["saved"] += add_amt
                        _persist()
                        st.rerun()
            with bc3:
                if st.button("🗑", key=f"delbig_{idx}", use_container_width=True):
                    st.session_state.big_plans.pop(idx)
                    _persist()
                    st.rerun()
    else:
        st.markdown('<div class="alert-card-neutral" style="text-align:center;padding:24px;"><div style="font-family:Share Tech Mono,monospace;color:#5a7a8a;font-size:0.75rem;">尚無預存計畫<br>新增你的第一個大額支出目標</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AUTO-SAVE ALL APP DATA TO LOCALSTORAGE
# ─────────────────────────────────────────────
_all_data = _json.dumps({
    "snap": _encode(st.session_state.snapshots),
    "dca":  _encode(st.session_state.dca_records),
    "fun":  _encode(st.session_state.fun_exp),
    "big":  _encode(st.session_state.big_plans),
    "fcfg": _encode({"budget": st.session_state.fun_budget}),
})
st.components.v1.html(f"""<script>
(function(){{
  try {{
    var d = {_all_data};
    var p = window.parent;
    Object.keys(d).forEach(function(k){{ p.localStorage.setItem("fire_data_"+k, d[k]); }});
  }} catch(e) {{}}
}})();
</script>""", height=0)



# ─────────────────────────────────────────────
# ROW 9 — 月薪配置儀表板 SALARY ALLOCATOR
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="section-header">[ 09 ]  月薪配置儀表板 · SALARY ALLOCATOR</div>', unsafe_allow_html=True)

if "salary_cfg" not in st.session_state:
    _scfg = _decode(st.query_params.get("scfg", ""), {})
    st.session_state.salary_cfg = {
        "salary":        _scfg.get("salary",        60000),
        "dca_amt":       _scfg.get("dca_amt",        30000),
        "living":        _scfg.get("living",         15000),
        "emergency_pct": _scfg.get("emergency_pct",  5),
        "rigid":         _scfg.get("rigid", [
            {"name":"房租","amount":0},{"name":"保險","amount":0},
            {"name":"電信費","amount":0},{"name":"訂閱服務","amount":0},
        ]),
    }

sal = st.session_state.salary_cfg
sal_col1, sal_col2 = st.columns([2, 3])

with sal_col1:
    new_salary = st.number_input("月薪實領 (TWD)", min_value=0, value=sal["salary"], step=1000, key="sal_salary")
    new_dca    = st.number_input("定期定額 00631L", min_value=0, value=sal["dca_amt"], step=1000, key="sal_dca")
    new_living = st.number_input("生活費預算", min_value=0, value=sal["living"], step=500, key="sal_living")
    new_ep     = st.number_input("緊急備用金提撥 (%)", min_value=0, max_value=30, value=sal["emergency_pct"], step=1, key="sal_ep",
                                  help="建議 3-5%，目標 = 6 個月生活費")
    st.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:0.65rem;color:#5a7a8a;margin:8px 0 4px;">剛性支出明細</div>', unsafe_allow_html=True)
    rigid_items = sal["rigid"].copy()
    updated_rigid = []
    for i, item in enumerate(rigid_items):
        rc1, rc2 = st.columns([3, 2])
        with rc1: nm = st.text_input(f"項目{i+1}", value=item["name"], key=f"rname_{i}", label_visibility="collapsed")
        with rc2: am = st.number_input(f"金額{i+1}", min_value=0, value=item["amount"], step=100, key=f"ramt_{i}", label_visibility="collapsed")
        updated_rigid.append({"name": nm, "amount": am})
    rc1, rc2 = st.columns(2)
    with rc1:
        if st.button("➕ 新增", use_container_width=True, key="rigid_add"):
            updated_rigid.append({"name":"新項目","amount":0})
    with rc2:
        if st.button("🗑 刪除", use_container_width=True, key="rigid_del") and updated_rigid:
            updated_rigid.pop()
    st.session_state.salary_cfg = {"salary":new_salary,"dca_amt":new_dca,"living":new_living,"emergency_pct":new_ep,"rigid":updated_rigid}
    st.query_params.update({"scfg": _encode(st.session_state.salary_cfg)})

with sal_col2:
    sal         = st.session_state.salary_cfg
    salary      = sal["salary"]
    dca_amt     = sal["dca_amt"]
    living_amt  = sal["living"]
    ep_amt      = round(salary * sal["emergency_pct"] / 100)
    fun_amt_cfg = st.session_state.fun_budget
    rigid_total = sum(r["amount"] for r in sal["rigid"])
    loan_int_mo = round(monthly_interest)
    total_alloc = dca_amt + living_amt + ep_amt + fun_amt_cfg + rigid_total + loan_int_mo
    remainder   = salary - total_alloc
    rem_col     = "#00ff88" if remainder >= 0 else "#ff3366"

    pie_labels = ["定期定額","剛性支出","生活費","娛樂基金","緊急備用金","質押利息","結餘"]
    pie_vals   = [dca_amt, rigid_total, living_amt, fun_amt_cfg, ep_amt, loan_int_mo, max(remainder,0)]
    pie_colors = ["#00ff88","#ff6688","#00d4ff","#ffaa00","#aa88ff","#ff3366","#1e3a4a"]

    pie_html = f"""<html><body style="margin:0;background:transparent;display:flex;gap:12px;align-items:center;padding:4px 0;">
<canvas id="pc" width="150" height="150"></canvas>
<div id="lg" style="font-family:Share Tech Mono,monospace;font-size:0.62rem;line-height:1.9;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<script>
var lb={_json.dumps(pie_labels)},vl={_json.dumps(pie_vals)},cl={_json.dumps(pie_colors)};
var lg=document.getElementById('lg');
lb.forEach(function(l,i){{if(vl[i]>0)lg.innerHTML+='<div><span style="color:'+cl[i]+'">■</span> '+l+' $'+vl[i].toLocaleString()+'</div>';}});
new Chart(document.getElementById('pc').getContext('2d'),{{type:'doughnut',data:{{labels:lb,datasets:[{{data:vl,backgroundColor:cl,borderWidth:0}}]}},options:{{responsive:false,plugins:{{legend:{{display:false}}}}}}}});
</script></body></html>"""
    st.components.v1.html(pie_html, height=165)

    items = [
        ("定期定額 00631L", dca_amt,     "#00ff88", "📈 複利引擎，優先扣款"),
        ("剛性支出",        rigid_total,  "#ff6688", "🏠 " + " · ".join([f"{r['name']} {r['amount']:,}" for r in sal["rigid"] if r["amount"]>0]) or "固定費用"),
        ("生活費",          living_amt,   "#00d4ff", "🛒 飲食、交通、日常"),
        ("娛樂基金",        fun_amt_cfg,  "#ffaa00", "🎮 每月限額控管"),
        ("緊急備用金提撥",  ep_amt,       "#aa88ff", f"🛡 薪資{sal['emergency_pct']}%，目標6個月生活費"),
        ("質押月利息",      loan_int_mo,  "#ff3366", f"🏦 年利率{pledge_rate:.2f}%"),
    ]
    rows_html = ""
    for name, amt, col, note in items:
        pct = amt/salary*100 if salary > 0 else 0
        rows_html += f"""<tr style="border-bottom:1px solid #1a2a3a;">
          <td style="padding:8px 12px;font-family:Share Tech Mono,monospace;color:{col};font-size:0.78rem;">{name}</td>
          <td style="padding:8px 12px;font-family:Share Tech Mono,monospace;color:#e8f4f8;font-size:0.78rem;text-align:right;">${amt:,}</td>
          <td style="padding:8px 12px;font-family:Share Tech Mono,monospace;color:#5a7a8a;font-size:0.72rem;text-align:right;">{pct:.1f}%</td>
          <td style="padding:8px 12px;font-family:Share Tech Mono,monospace;color:#2a4a5a;font-size:0.65rem;">{note}</td>
        </tr>"""
    rem_advice = f"💡 下月加碼 00631L 或存備用金" if remainder > 0 else (f"⚠ 超支 ${abs(remainder):,}" if remainder < 0 else "✅ 收支平衡")
    st.markdown(f"""<div class="alert-card-neutral">
      <table style="width:100%;border-collapse:collapse;">
        <thead><tr style="border-bottom:2px solid #1e3a4a;">
          <th style="padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:0.6rem;color:#5a7a8a;text-align:left;">配置項目</th>
          <th style="padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:0.6rem;color:#5a7a8a;text-align:right;">金額</th>
          <th style="padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:0.6rem;color:#5a7a8a;text-align:right;">佔薪</th>
          <th style="padding:8px 12px;font-family:Share Tech Mono,monospace;font-size:0.6rem;color:#5a7a8a;text-align:left;">說明</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
        <tfoot><tr style="border-top:2px solid #1e3a4a;">
          <td style="padding:10px 12px;font-family:Orbitron,monospace;font-size:0.8rem;color:#00d4ff;">本月結餘</td>
          <td style="padding:10px 12px;font-family:Share Tech Mono,monospace;font-size:1rem;color:{rem_col};text-align:right;font-weight:bold;">${remainder:,}</td>
          <td style="padding:10px 12px;font-family:Share Tech Mono,monospace;font-size:0.8rem;color:{rem_col};text-align:right;">{remainder/salary*100:.1f}%</td>
          <td style="padding:10px 12px;font-family:Share Tech Mono,monospace;font-size:0.7rem;color:{rem_col};">{rem_advice}</td>
        </tfoot>
      </table></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 10 — 獎金配置器 BONUS ALLOCATOR
# ─────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="section-header">[ 10 ]  獎金配置器 · BONUS ALLOCATOR</div>', unsafe_allow_html=True)

bon_c1, bon_c2 = st.columns([2, 3])

with bon_c1:
    bonus_type   = st.selectbox("獎金類型", ["年終獎金","績效獎金","分紅","其他"], key="bonus_type")
    bonus_amount = st.number_input("獎金金額 (稅前)", min_value=0, value=100000, step=10000, key="bonus_amount")
    bonus_tax    = st.number_input("預估稅率 (%)", min_value=0, max_value=40, value=10, step=1, key="bonus_tax",
                                    help="獎金通常含 10% 二代健保補充保費＋所得稅")
    st.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:0.65rem;color:#5a7a8a;margin:10px 0 4px;">配置明細</div>', unsafe_allow_html=True)
    bon_pledge    = st.number_input("① 提前還質押借款", min_value=0, value=0, step=10000, key="bon_pledge",
                                     help=f"目前質押 ${pledge_loan:,}，還款可降低利息")
    bon_emergency = st.number_input("② 補充緊急備用金", min_value=0, value=0, step=5000, key="bon_emergency",
                                     help="建議目標：6 個月生活費")
    bon_bigfill   = st.number_input("③ 填補大額支出計畫", min_value=0, value=0, step=5000, key="bon_bigfill")
    bon_dca_extra = st.number_input("④ 加碼 00631L", min_value=0, value=0, step=5000, key="bon_dca",
                                     help="一次性加碼，加速 100 萬達成")
    bon_save      = st.number_input("⑤ 存定存/備用現金", min_value=0, value=0, step=5000, key="bon_save")

with bon_c2:
    after_tax    = round(bonus_amount * (1 - bonus_tax / 100))
    total_alloc  = bon_pledge + bon_emergency + bon_bigfill + bon_dca_extra + bon_save
    unalloc      = after_tax - total_alloc
    unalloc_col  = "#00ff88" if unalloc >= 0 else "#ff3366"
    bar_pct      = min(total_alloc / after_tax * 100, 100) if after_tax > 0 else 0
    interest_saved = bon_pledge * (pledge_rate / 100)
    cur_dca_val  = (p_00631L or 0) * shares_00631L
    new_dca_val  = cur_dca_val + bon_dca_extra
    new_dca_pct  = min(new_dca_val / 1_000_000 * 100, 100)
    em_target    = st.session_state.salary_cfg["living"] * 6

    st.markdown(f"""<div class="alert-card-neutral">
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:14px;">
        <div><div class="kpi-label">稅後到手</div>
          <div style="font-family:Orbitron,monospace;font-size:1.1rem;color:#00d4ff;">${after_tax:,}</div>
          <div class="kpi-sub">稅率 {bonus_tax}%</div></div>
        <div><div class="kpi-label">已配置</div>
          <div style="font-family:Orbitron,monospace;font-size:1.1rem;color:#ffaa00;">${total_alloc:,}</div>
          <div class="kpi-sub">{bar_pct:.1f}%</div></div>
        <div><div class="kpi-label">未配置餘額</div>
          <div style="font-family:Orbitron,monospace;font-size:1.1rem;color:{unalloc_col};">${unalloc:,}</div>
          <div class="kpi-sub">{'✅ 仍有結餘' if unalloc >= 0 else '⚠ 超出'}</div></div>
      </div>
      <div class="progress-wrap" style="margin-bottom:14px;">
        <div class="progress-fill-green" style="width:{bar_pct:.1f}%;"></div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px;">
        <div style="background:#080c10;border:1px solid #1e3a4a;border-radius:6px;padding:12px;">
          <div class="kpi-label">加碼後 00631L 進度</div>
          <div style="font-family:Share Tech Mono,monospace;font-size:1rem;color:#00ff88;">{new_dca_pct:.1f}%</div>
          <div class="progress-wrap"><div class="progress-fill-green" style="width:{new_dca_pct:.1f}%;"></div></div>
          <div class="kpi-sub">${new_dca_val:,.0f} / $1,000,000</div>
        </div>
        <div style="background:#080c10;border:1px solid #1e3a4a;border-radius:6px;padding:12px;">
          <div class="kpi-label">還款後每年省息</div>
          <div style="font-family:Share Tech Mono,monospace;font-size:1rem;color:#00ff88;">${interest_saved:,.0f}</div>
          <div class="kpi-sub">還款 ${bon_pledge:,} × {pledge_rate:.2f}%</div>
        </div>
      </div>
      <div style="border-top:1px solid #1e3a4a;padding-top:10px;">
        <div style="font-family:Share Tech Mono,monospace;font-size:0.65rem;color:#5a7a8a;line-height:2.1;">
          <span style="color:#00d4ff;">📋 建議優先順序</span><br>
          <span style="color:#aa88ff;">① 緊急備用金</span> — 目標 {em_target:,} TWD（6個月生活費），先補滿安全網<br>
          <span style="color:#00ff88;">② 加碼 00631L</span> — 距 100 萬目標差 ${max(1_000_000-cur_dca_val,0):,.0f}，獎金是最快捷徑<br>
          <span style="color:#ff6688;">③ 還款評估</span> — 每還 10 萬年省 ${100000*pledge_rate/100:,.0f}，報酬率 {pledge_rate:.2f}%<br>
          <span style="color:#ffaa00;">④ 大額計畫</span> — 填補最近到期的支出計畫，免臨時動用投資<br>
          <span style="color:#1e3a4a;background:#00d4ff;padding:0 4px;border-radius:2px;">⑤ 定存</span> — 確定短期內會用到的資金才存定存，其餘投入 006208
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    if unalloc > 0:
        best_use = "加碼 00631L" if new_dca_pct < 100 else "補充 006208 持倉"
        st.markdown(f"""<div class="alert-card-green" style="margin-top:8px;">
          <div style="font-family:Share Tech Mono,monospace;font-size:0.75rem;color:#00ff88;">
            💡 還有 ${unalloc:,} 未配置 — 建議用於：{best_use}
          </div></div>""", unsafe_allow_html=True)
    elif unalloc < 0:
        st.markdown(f"""<div class="alert-card-red" style="margin-top:8px;">
          <div style="font-family:Share Tech Mono,monospace;font-size:0.75rem;color:#ff3366;">
            ⚠ 配置超出稅後獎金 ${abs(unalloc):,}，請調整各項金額
          </div></div>""", unsafe_allow_html=True)


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
