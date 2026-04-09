import streamlit as st
import sys, os, time, random, requests, hashlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.strategies import get_strategy
from core.advanced_agents import RiskAgent
from core.ml_forecaster import GasForecaster
from core.defi_optimizer import DeFiOptimizer
from core.contract_analyzer import ContractAnalyzer
from core.cross_chain import CrossChainComparator

st.set_page_config(page_title="TON Gas Optimizer AI", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# ========== STATE ==========
if "dark_mode" not in st.session_state: st.session_state.dark_mode = False
if "connected" not in st.session_state: st.session_state.connected = False
if "addr" not in st.session_state: st.session_state.addr = ""
if "bal" not in st.session_state: st.session_state.bal = 0.0
if "demo" not in st.session_state: st.session_state.demo = False
if "network_mode" not in st.session_state: st.session_state.network_mode = os.getenv("NETWORK", "testnet").lower()
if "ops" not in st.session_state: st.session_state.ops = 5
if "strategy" not in st.session_state: st.session_state.strategy = "default"
if "opt_result" not in st.session_state: st.session_state.opt_result = None
if "backtest_result" not in st.session_state: st.session_state.backtest_result = None
if "defi_result" not in st.session_state: st.session_state.defi_result = None
if "contract_result" not in st.session_state: st.session_state.contract_result = None
if "roi_data" not in st.session_state: st.session_state.roi_data = None
if "api_status" not in st.session_state: st.session_state.api_status = "🎭 Simulated"
if "ton_price_usd" not in st.session_state: st.session_state.ton_price_usd = 0.0
if "api_key" not in st.session_state: st.session_state.api_key = os.getenv("TONCENTER_API_KEY", "")

API_ENDPOINTS = {
    "testnet": {"base": "https://testnet.toncenter.com/api/v2", "label": "TESTNET", "key_required": False},
    "mainnet": {"base": "https://toncenter.com/api/v2", "label": "MAINNET", "key_required": True}
}

# ========== JS НАБЛЮДАТЕЛЬ ==========
st.components.v1.html("""
<script>
(function() {
  const observer = new MutationObserver(mutations => {
    mutations.forEach(m => {
      m.addedNodes.forEach(node => {
        if (node.nodeType === 1) {
          const process = (el) => {
            if (el.matches && el.matches('[data-baseweb="menu"]') && !el.dataset.smooth) {
              el.dataset.smooth = '1';
              el.style.opacity = '0';
              el.style.transform = 'scale(0.96) translateY(-6px)';
              el.style.transition = 'none';
              void el.offsetWidth;
              el.style.transition = 'opacity 0.32s cubic-bezier(0.4, 0, 0.2, 1), transform 0.32s cubic-bezier(0.4, 0, 0.2, 1)';
              requestAnimationFrame(() => {
                el.style.opacity = '1';
                el.style.transform = 'scale(1) translateY(0)';
              });
            }
            if (el.querySelectorAll) el.querySelectorAll('[data-baseweb="menu"]').forEach(process);
          };
          process(node);
        }
      });
    });
  });
  if (document.body) observer.observe(document.body, { childList: true, subtree: true });
  else document.addEventListener('DOMContentLoaded', () => observer.observe(document.body, { childList: true, subtree: true }));
})();
</script>
""", height=0, width=0)

# ========== CSS ==========
CSS_LIGHT = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* {font-family: 'Inter', sans-serif;}
.stApp, .stAlert, .stMetric, .stTextInput, .stNumberInput, section[data-testid="stSidebar"], .stTabs [data-baseweb="tab"] {
    transition: background-color 0.5s cubic-bezier(0.4, 0, 0.2, 1), color 0.5s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.stApp {background: linear-gradient(135deg, #F9F7F4 0%, #F5F0E8 100%) !important;}
footer {visibility: hidden;}
footer:after {content: 'MIT 2026'; visibility: visible; display: block; position: fixed; bottom: 15px; left: 20px; color: #9CA3AF !important;}
h1,h2,h3 {color: #111827 !important;}
.stMarkdown p, label {color: #4B5563 !important;}
.stAlert, .stAlert * { background-color: #FFFFFF !important; color: #111827 !important; border: 1px solid #E5E7EB !important; border-radius: 12px !important; }
.stAlert svg {color: #111827 !important;}
.stAlert code {background: #F3F4F6 !important; color: #111827 !important;}
div.stButton > button {background: linear-gradient(135deg, #F97316, #EA580C) !important; color: #FFF !important; border: none !important; border-radius: 10px !important; padding: 8px 20px !important; font-weight: 600 !important; transition: all 0.3s ease !important;}
div.stButton > button:hover {transform: translateY(-2px) !important; box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3) !important;}
.stTextInput > div > div > input, .stNumberInput > div > div > input {background: #FFF !important; color: #111827 !important; border: 2px solid #E5E7EB !important; border-radius: 10px !important;}
.stMetric {background: #FFFFFF !important; border-radius: 14px !important; padding: 1.2rem !important; border: 1px solid #F3F4F6 !important;}
[data-testid="stMetricValue"] {color: #F97316 !important;}
[data-testid="stMetricLabel"] {color: #6B7280 !important;}
section[data-testid="stSidebar"] {background: #FAF9F7 !important; border-right: 1px solid #E5E7EB !important;}
.stTabs [data-baseweb="tab"] {background: #FFFFFF !important; border: 1px solid #E5E7EB !important; border-radius: 10px !important; color: #6B7280 !important;}
.stTabs [data-baseweb="tab"][aria-selected="true"] {background: linear-gradient(135deg, #F97316, #EA580C) !important; color: #FFF !important; border-color: #EA580C !important;}
</style>"""

CSS_DARK = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* {font-family: 'Inter', sans-serif;}
.stApp, .stAlert, .stMetric, .stTextInput, .stNumberInput, section[data-testid="stSidebar"], .stTabs [data-baseweb="tab"] {
    transition: background-color 0.5s cubic-bezier(0.4, 0, 0.2, 1), color 0.5s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.stApp {background: linear-gradient(135deg, #0B0F19 0%, #151B28 100%) !important;}
footer {visibility: hidden;}
footer:after {content: 'MIT 2026'; visibility: visible; display: block; position: fixed; bottom: 15px; left: 20px; color: #6B7280 !important;}
h1,h2,h3 {color: #FFFFFF !important;}
.stMarkdown p, label {color: #D1D5DB !important;}
.stAlert, .stAlert * { background-color: #1F2937 !important; color: #FFFFFF !important; border: 1px solid #374151 !important; border-radius: 12px !important; }
.stAlert svg {color: #FFFFFF !important;}
.stAlert code {background: #111827 !important; color: #E5E7EB !important;}
div.stButton > button {background: linear-gradient(135deg, #818CF8, #6366F1) !important; color: #FFF !important; border: none !important; border-radius: 10px !important; padding: 8px 20px !important; font-weight: 600 !important; transition: all 0.3s ease !important;}
div.stButton > button:hover {transform: translateY(-2px) !important; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4) !important;}
.stTextInput > div > div > input, .stNumberInput > div > div > input {background: #111827 !important; color: #FFFFFF !important; border: 2px solid #374151 !important; border-radius: 10px !important;}
.stTextInput > div > div > input::placeholder, .stNumberInput > div > div > input::placeholder { color: #FFFFFF !important; opacity: 0.7 !important; }
.stMetric {background: #1F2937 !important; border-radius: 14px !important; padding: 1.2rem !important; border: 1px solid #374151 !important;}
[data-testid="stMetricValue"] {color: #818CF8 !important;}
[data-testid="stMetricLabel"] {color: #9CA3AF !important;}
section[data-testid="stSidebar"] {background: #0B0F19 !important; border-right: 1px solid #1F2937 !important;}
.stTabs [data-baseweb="tab"] {background: #1F2937 !important; border: 1px solid #374151 !important; border-radius: 10px !important; color: #9CA3AF !important;}
.stTabs [data-baseweb="tab"][aria-selected="true"] {background: linear-gradient(135deg, #818CF8, #6366F1) !important; color: #FFF !important; border-color: #6366F1 !important;}
</style>"""

if st.session_state.dark_mode: st.markdown(CSS_DARK, unsafe_allow_html=True)
else: st.markdown(CSS_LIGHT, unsafe_allow_html=True)

# ========== API ФУНКЦИИ С КЛЮЧОМ ==========
def _get_mock(addr, base, var):
    seed = int(hashlib.md5(addr.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    return round(base + random.uniform(-var, var), 4)

@st.cache_data(ttl=60)
def fetch_gas_price(base, api_key=""):
    try:
        params = {"id": "21"}
        if api_key: params["api_key"] = api_key
        r = requests.get(f"{base}/getConfig", params=params, timeout=15)
        if r.status_code == 200: return int(r.json().get("result", {}).get("gas_price", 5000)), True
    except: pass
    return 5000, False

@st.cache_data(ttl=30)
def fetch_balance(addr, base, api_key="", demo=False):
    if demo: return _get_mock(addr, 25.0, 5.0), True, None
    if not addr or len(addr) < 40: return None, False, "Invalid address"
    
    try:
        params = {"address": addr}
        if api_key: params["api_key"] = api_key
        
        r = requests.get(f"{base}/getAddressBalance", params=params, timeout=15)
        
        if r.status_code == 401:
            return None, False, "Invalid or missing API key"
        elif r.status_code == 429:
            return None, False, "Rate limit exceeded. Try again later."
        elif r.status_code != 200:
            return None, False, f"HTTP {r.status_code}: {r.text[:100]}"
        
        d = r.json()
        if "result" in d and isinstance(d["result"], dict) and "balance" in d["result"]:
            return int(d["result"]["balance"])/1e9, True, None
        if "result" in d and isinstance(d["result"], str):
            return int(d["result"])/1e9, True, None
        if "balance" in d:
            return int(d["balance"])/1e9, True, None
        
        return None, False, f"Unexpected response: {d}"
        
    except requests.exceptions.Timeout:
        return None, False, "Connection timeout. Check your internet."
    except requests.exceptions.ConnectionError:
        return None, False, "Cannot connect to API. Check firewall/proxy."
    except Exception as e:
        return None, False, f"Error: {str(e)[:150]}"

@st.cache_data(ttl=30)
def fetch_ton_price_usd():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json().get("the-open-network", {}).get("usd", 0.0)
    except: pass
    return 0.0

# Инициализация
base_url = API_ENDPOINTS[st.session_state.network_mode]["base"]
network_label = API_ENDPOINTS[st.session_state.network_mode]["label"]
gas_price, api_live = fetch_gas_price(base_url, st.session_state.api_key)
if api_live: st.session_state.api_status = "✅ Live"
st.session_state.ton_price_usd = fetch_ton_price_usd()

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("### 🎨 Theme")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("☀️ Light", use_container_width=True, key="btn_light"):
            st.session_state.dark_mode = False
            st.rerun()
    with col2:
        if st.button("🌙 Dark", use_container_width=True, key="btn_dark"):
            st.session_state.dark_mode = True
            st.rerun()
    
    st.title("⚡ TON Optimizer")
    st.caption("AI-Powered Gas Reduction")
    st.divider()
    
    # ✅ ПОЛЕ ДЛЯ API КЛЮЧА
    st.markdown("### 🔑 API Key")
    api_key_input = st.text_input(
        "toncenter.com API Key",
        value=st.session_state.api_key,
        type="password",
        help="Get free API key at https://toncenter.com (required for Mainnet)",
        key="api_key_input"
    )
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        st.rerun()
    
    if st.session_state.api_key:
        st.success("✅ API key saved")
        if st.button("🗑️ Clear key", key="clear_api_key"):
            st.session_state.api_key = ""
            st.rerun()
    else:
        if st.session_state.network_mode == "mainnet":
            st.warning("⚠️ **Required for Mainnet**")
        else:
            st.info("ℹ️ Optional for Testnet")
    
    st.divider()
    
    if st.session_state.ton_price_usd > 0:
        st.markdown(f"📊 **1 TON = ${st.session_state.ton_price_usd:.2f}**")
        st.divider()
    
    st.markdown("### 🌐 Network")
    net = st.selectbox("Environment", ["testnet", "mainnet"], index=0 if st.session_state.network_mode=="testnet" else 1, key="net_sel")
    if net != st.session_state.network_mode: st.session_state.network_mode = net
    st.markdown(f"{'🟢' if st.session_state.network_mode=='mainnet' else '🟠'} **{network_label}**")
    st.info(f"Status: {st.session_state.api_status} | Gas: `{gas_price}` nano")
    st.divider()
    st.session_state.ops = st.number_input("Operations", 1, 100, st.session_state.ops, key="ops_input")
    st.session_state.strategy = st.selectbox("Strategy", ["default", "aggressive", "conservative"], key="strat_sel")
    st.divider()
    risk = RiskAgent().evaluate(st.session_state.bal, st.session_state.ops*0.005, 42)
    st.markdown("### 🛡️ Risk")
    st.metric("Level", risk["risk_level"])
    st.progress(risk["risk_score"])

# ========== HEADER ==========
c1, c2 = st.columns([3, 1])
with c1: st.title("⚡ TON Gas Optimizer + AI"); st.info(f"Environment: **{network_label}**")
with c2:
    usd_balance = st.session_state.bal * st.session_state.ton_price_usd
    
    if not st.session_state.connected:
        addr = st.text_input("Wallet Address", placeholder="UQ... or EQ... (48 chars)", key="addr_input", help="Enter valid TON wallet address")
        col_r, col_d = st.columns(2)
        with col_r:
            if st.button("🔗 Real", type="primary", key="btn_real"):
                if addr and len(addr) >= 40:
                    with st.spinner("Connecting to blockchain..."):
                        bal, ok, err = fetch_balance(addr, base_url, st.session_state.api_key, demo=False)
                        if ok and bal is not None: 
                            st.session_state.update({"connected": True, "addr": addr, "bal": bal, "demo": False})
                            st.success(f"✅ Connected: {bal:.4f} TON")
                            st.rerun()
                        else: 
                            st.error(f"❌ {err}")
                            if "API key" in err.lower():
                                st.info("💡 Go to sidebar → enter API key → try again")
                            elif "timeout" in err.lower():
                                st.info("💡 Try Demo mode or check internet connection")
                else: st.error("⚠️ Address must be 40+ characters")
        with col_d:
            if st.button("🎭 Demo", key="btn_demo"):
                if addr and len(addr) >= 40:
                    bal, _, _ = fetch_balance(addr, base_url, st.session_state.api_key, demo=True)
                    st.session_state.update({"connected": True, "addr": addr, "bal": bal, "demo": True})
                    st.success(f"🎭 Demo: {bal:.4f} TON")
                    st.rerun()
                else: st.error("⚠️ Address must be 40+ characters")
    else:
        mode = "🎭 Demo" if st.session_state.demo else "🟢 Real"
        bg_color = "#FFFFFF" if not st.session_state.dark_mode else "#1F2937"
        txt_color = "#111827" if not st.session_state.dark_mode else "#FFFFFF"
        st.markdown(f"""
        <div style="background-color: {bg_color}; border-radius: 14px; padding: 1rem; border: 1px solid {'#E5E7EB' if not st.session_state.dark_mode else '#374151'}; margin-bottom: 1rem;">
            <span style="color: {txt_color}; font-weight: 600;">🟢 {mode}</span><br>
            <code style="color: {'#6B7280' if not st.session_state.dark_mode else '#9CA3AF'}; font-size: 0.85em;">{st.session_state.addr[:16]}...</code>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Balance", f"{st.session_state.bal:.4f} TON", delta=f"≈ ${usd_balance:.2f} USD")
        if st.button("🔌 Disconnect", key="btn_disconnect"): 
            st.session_state.update({"connected": False, "addr": "", "bal": 0.0, "demo": False})
            st.rerun()

# ========== TABS ==========
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 Optimization", "🧪 Backtest", "📊 DeFi", "🔍 Contract", "🌍 Cross-Chain"])
with tab1:
    st.markdown("### 🚀 AI Optimization")
    if st.button("⚡ Run", type="primary", disabled=not st.session_state.connected, key="btn_opt"):
        with st.spinner("Analyzing..."):
            time.sleep(0.5)
            strat = get_strategy(st.session_state.strategy)
            st.session_state.opt_result = {"batch": strat.should_batch(st.session_state.ops, 42, gas_price), "savings": strat.estimate_savings(st.session_state.ops, gas_price, 42), "reason": strat.get_reason(st.session_state.ops, 42, gas_price), "conf": 85+random.randint(0,10)}
    if st.session_state.opt_result:
        r = st.session_state.opt_result; c1,c2,c3 = st.columns(3)
        c1.success("✅ BATCH" if r["batch"] else "❌ SEND"); c2.metric("Savings", f"{r['savings']:.1f}%"); c3.metric("Confidence", f"{r['conf']}%")
        st.info(f"💡 {r['reason']}")
with tab2:
    st.markdown("### 🧪 Backtest")
    if st.button("🔄 Run Backtest", key="btn_back"):
        try:
            from core.backtest import GasBacktester
            with st.spinner("Simulating..."):
                bt = GasBacktester(); df = bt.generate_mock_history(7); res = bt.simulate_strategy(df, get_strategy("default").should_batch)
                st.success(f"💰 Saved: **{bt.get_summary(res)['total_saved_ton']:.4f} TON**"); st.line_chart(df.set_index("timestamp")["gas_price"])
        except: st.error("❌ Backtest module not available")
with tab3:
    st.markdown("### 📊 DeFi Router")
    ca,cb,cc = st.columns(3)
    with ca: amt = st.number_input("Amount (TON)", 0.1, 1000.0, 10.0, 1.0, key="defi_amt")
    with cb: pair = st.selectbox("Pair", ["TON/USDT", "TON/NOT", "TON/DOGS"], key="defi_pair")
    with cc: slip = st.slider("Slippage %", 0.1, 2.0, 0.5, 0.1, key="defi_slip")
    if st.button("🔍 Analyze", type="primary", key="btn_defi"):
        with st.spinner("Routing..."): st.session_state.defi_result = DeFiOptimizer().analyze_swap(amt, pair, slip)
    if st.session_state.defi_result:
        r = st.session_state.defi_result; m1,m2,m3,m4 = st.columns(4)
        m1.metric("Output", f"{r['estimated_output']}"); m2.metric("Fee", f"{r['dex_fee']}"); m3.metric("Gas", f"{r['gas_cost']}"); m4.metric("Impact", f"{r['price_impact']}%")
        st.success(f"🛣️ {r['route']}")
with tab4:
    st.markdown("### 🔍 Contract & ROI")
    code = st.text_area("FunC Code", value=st.session_state.get("contract_code",""), height=100, placeholder="fun swap() { ... }", key="code_area")
    if st.button("🔍 Analyze", type="primary", key="btn_analyze") and code.strip(): st.session_state.contract_result = ContractAnalyzer().analyze(code)
    if st.session_state.contract_result:
        r = st.session_state.contract_result; c1,c2,c3,c4 = st.columns(4)
        c1.metric("Complexity", r["complexity_level"]); c2.metric("Score", f"{r['score']}/100"); c3.metric("Gas", f"{r['estimated_gas_nano']}"); c4.metric("Batch", "✅" if r["safe_to_batch"] else "⚠️")
        for p in r["patterns_detected"]: st.warning(f"**{p['category']}** x{p['count']}")
        for rec in r["recommendations"]: st.info(rec)
with tab5:
    st.markdown("### 🌍 Cross-Chain")
    cmp = CrossChainComparator()
    tx_type = st.radio("Type", ["swap", "transfer", "mint"], horizontal=True, key="cross_type")
    if st.button("📊 Compare", type="primary", key="btn_compare"):
        df = cmp.get_comparison_table(tx_type); st.dataframe(df, use_container_width=True)
        sav = cmp.calculate_savings(tx_type, 100); st.success(f"💡 Save **${sav['savings_usd']:.2f}** vs ETH")
st.markdown("---"); st.caption(f"MIT 2026 • Open Source • {network_label} • {st.session_state.api_status}")
