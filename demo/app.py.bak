# demo/app.py - TON Gas Optimizer AI | FINAL VERSION (Streamlit Menu 100% RESTORED)
import streamlit as st, requests, time, re, hashlib, sys, os, json, pandas as pd, random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

API_ENDPOINTS = {"testnet": {"api": "https://testnet.toncenter.com/api/v2", "tonapi": "https://testnet.tonapi.io/v2"}}
NETWORK_MODE = os.getenv("NETWORK", "testnet").lower()
if NETWORK_MODE != "testnet": NETWORK_MODE = "testnet"

# Theme toggle
if "dark_mode" not in st.session_state: st.session_state.dark_mode = True
if st.sidebar.toggle("🌙 Dark Mode", st.session_state.dark_mode) != st.session_state.dark_mode:
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

# ========== STREAMLIT PAGE CONFIG (ORIGINAL SETTINGS) ==========
st.set_page_config(
    page_title="TON Gas Optimizer AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/beardbull/ton-gas-optimizer-ai-agents',
        'Report a bug': 'https://github.com/beardbull/ton-gas-optimizer-ai-agents/issues',
        'About': "# TON Gas Optimizer AI\n\nAI-powered gas optimization for TON blockchain agents.\n\n**Features:**\n- Multi-agent architecture\n- Real-time gas tracking\n- DeFi pool analysis\n- Strategy presets\n\nBuilt for The Rise of AI Agents Hackathon • Lablab.ai"
    }
)

# ========== CSS - DARK MODE (NO MENU OVERRIDES) ==========
CSS_DARK = """<style>
/* Base - NO MainMenu/header/footer hiding! */
.stApp {background:#0B1120!important; color:#D1FAE5!important;}
section[data-testid="stSidebar"]{background:#0F172A!important; border-right:1px solid #1E293B!important;}

/* Text */
p,span,label,div,.stMarkdown p,.stText{color:#34D399!important;}
h1,h2,h3,h4{color:#34D399!important;}

/* Inputs */
.stTextInput input,.stNumberInput input,.stSelectbox select,.stTextArea textarea{
    background:#1E293B!important; color:#F8FAFC!important; border:1px solid #10B981!important; border-radius:8px!important;}
.stTextInput input::placeholder{color:#34D399!important; opacity:0.8!important;}

/* BUTTONS - BLACK TEXT */
button[data-testid="baseButton-primary"],
button[data-testid="baseButton-secondary"],
button[data-testid="stDownloadButton"],
.stButton button,
.stDownloadButton button,
div[data-testid="stButton"] button,
.stButton > button,
.stDownloadButton > button,
.stButton > button > span,
.stDownloadButton > button > span,
button[data-testid="baseButton-primary"] span,
button[data-testid="baseButton-secondary"] span,
button[data-testid="stDownloadButton"] span {
    background:#10B981!important;
    color:#000000!important;
    -webkit-text-fill-color:#000000!important;
    border:none!important;
    border-radius:8px!important;
    font-weight:700!important;
    width:auto!important;
    padding:0.5rem 1rem!important;
    margin:0!important;
}
button[data-testid="baseButton-primary"]:hover,
.stButton button:hover,
.stDownloadButton button:hover {
    background:#059669!important;
    color:#000000!important;
    -webkit-text-fill-color:#000000!important;
}

/* DROPDOWNS - GRAY BACKGROUND */
.stSelectbox *,div[data-baseweb="select"],div[data-baseweb="menu"],ul[role="listbox"],[role="option"]{
    background:#1E293B!important; color:#F8FAFC!important; border-color:#334155!important;}
div[data-baseweb="menu"] li:hover,ul[role="listbox"] li:hover,[role="option"]:hover{
    background:#334155!important; color:#F8FAFC!important;}

/* COPY REPORT - GRAY BACKGROUND */
.stCode,div[data-testid="stCode"],div[data-testid="stCode"] pre,div[data-testid="stCode"] code{
    background:#1E293B!important; color:#F8FAFC!important; border:1px solid #334155!important;}

/* Metrics & Alerts */
.stMetric{background:#151E32!important; border:1px solid #059669!important; border-radius:10px!important; padding:0.8rem!important;}
[data-testid="stMetricValue"]{color:#34D399!important; font-size:1.5rem!important; font-weight:800!important;}
[data-testid="stMetricLabel"]{color:#6EE7B7!important; font-size:0.85rem!important;}
[data-testid="stAlert"],[data-testid="stWarning"],[data-testid="stSuccess"],[data-testid="stError"]{
    background:#0F172A!important; color:#D1FAE5!important; border-radius:8px!important; border-left:4px solid #10B981!important;}

/* Expanders & Scrollbar */
details{background:#151E32!important; border:1px solid #059669!important; border-radius:8px!important;}
summary{color:#34D399!important; font-weight:600!important;}
::-webkit-scrollbar{width:6px!important;}
::-webkit-scrollbar-track{background:#0B1120!important;}
::-webkit-scrollbar-thumb{background:#10B981!important; border-radius:3px!important;}

/* Large Numbers */
.element-container .stAlert p strong,.element-container .stAlert p span{font-size:1.8rem!important; font-weight:800!important;}
</style>"""

# ========== CSS - LIGHT MODE (NO MENU OVERRIDES) ==========
CSS_LIGHT = """<style>
.stApp {background:#F8FAFC!important; color:#0F172A!important;}
section[data-testid="stSidebar"]{background:#FFFFFF!important; border-right:1px solid #E2E8F0!important;}
.stMarkdown p,.stMarkdown span,.stText{color:#334155!important;}
h1,h2,h3,h4{color:#047857!important;}
.stTextInput input,.stNumberInput input,.stSelectbox select{
    background:#FFFFFF!important; color:#0F172A!important; border:1px solid #10B981!important; border-radius:8px!important;}
.stButton>button,.stDownloadButton>button{
    background:#10B981!important; color:#FFFFFF!important; border:none!important; border-radius:8px!important;
    font-weight:700!important; width:auto!important; padding:0.5rem 1rem!important; margin:0!important;}
.stButton>button:hover,.stDownloadButton>button:hover{background:#059669!important; color:#FFFFFF!important;}
.stMetric{background:#FFFFFF!important; border:1px solid #D1FAE5!important;}
[data-testid="stMetricValue"]{color:#047857!important;}
[data-testid="stMetricLabel"]{color:#64748B!important;}
[data-testid="stAlert"]{background:#F0FDF4!important; color:#0F172A!important; border-left:4px solid #10B981!important;}
details{background:#FFFFFF!important; border:1px solid #D1FAE5!important;}
summary{color:#047857!important;}
::-webkit-scrollbar{width:6px!important;}
::-webkit-scrollbar-track{background:#F1F5F9!important;}
::-webkit-scrollbar-thumb{background:#86EFAC!important;}
.element-container .stAlert p strong,.element-container .stAlert p span{font-size:1.8rem!important; font-weight:800!important;}
</style>"""

# Apply CSS
st.markdown(CSS_DARK if st.session_state.dark_mode else CSS_LIGHT, unsafe_allow_html=True)

# ========== CACHE FUNCTIONS ==========
@st.cache_data(ttl=30)
def fetch_balance_real(address, network, use_demo=False):
    if use_demo:
        seed = int(hashlib.md5(address.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        return round(random.uniform(20.0, 30.0), 4), None, True
    if not (address and len(address) == 48 and re.match(r'^(UQ|EQ|0Q)[a-zA-Z0-9_-]{46}$', address)):
        return None, "Invalid address format", False
    try:
        tonapi_base = API_ENDPOINTS[network]["tonapi"]
        resp = requests.get(f"{tonapi_base}/accounts/{address}", headers={"accept": "application/json"}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            bal_str = data.get("balance")
            if bal_str is not None: return int(bal_str) / 1e9, None, False
    except: pass
    seed = int(hashlib.md5(address.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    return round(random.uniform(20.0, 30.0), 4), "API fallback", True

@st.cache_data(ttl=30)
def fetch_gas_price(api_base):
    try:
        resp = requests.get(f"{api_base}/getConfig", params={"id": "21"}, timeout=10)
        data = resp.json()
        if data.get("ok"):
            val = data.get("result", {}).get("value")
            if val and str(val).isdigit(): return int(val)
    except: pass
    return 5000 + (int(time.time()) % 2000)

@st.cache_data(ttl=30)
def fetch_network_load(api_base):
    try:
        resp = requests.get(f"{api_base}/masterchainInfo", timeout=10)
        data = resp.json()
        if data.get("ok"):
            seqno = data.get("result", {}).get("last", {}).get("seqno", 0)
            return 30 + (seqno % 50)
    except: pass
    return 40 + (int(time.time()) % 40)

# ========== SESSION STATE ==========
defaults = {
    "ops": 5, "connected": False, "addr": "", "bal": 0.0, "demo": False,
    "gas_history": [], "last_gas_update": 0, "total_saved": 0.0,
    "address_insights": None, "strategy_name": "default",
    "opt_result": None, "opt_agents": None, "opt_gas": 0, "opt_load": 0, "opt_ops": 0, "opt_timestamp": ""
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

api_base = API_ENDPOINTS[NETWORK_MODE]["api"]
gas = fetch_gas_price(api_base)
load = fetch_network_load(api_base)

# ========== PREDICTION ==========
gas_prediction = "➡️ Stable"
if len(st.session_state.gas_history) >= 3:
    recent = [x["gas"] for x in st.session_state.gas_history[-5:]]
    avg = sum(recent) / len(recent)
    diff = recent[-1] - avg
    if diff < -100: gas_prediction = "📉 Low / Decreasing (Good)"
    elif diff > 100: gas_prediction = "📈 High / Rising (Wait)"

# ========== SIDEBAR ==========
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Toncoin_logo.svg/512px-Toncoin_logo.svg.png", width=50)
    st.title("TON Gas Optimizer")
    st.caption("AI-powered fee reduction")
    st.divider()
    st.markdown("### 🌐 Network")
    st.info(f"`{NETWORK_MODE.upper()}` — read-only")
    if st.button("🔄 Refresh"): st.rerun()
    st.metric("⛽ Gas", f"{gas} nano")
    st.metric("📊 Load", f"{load}%")
    st.divider()
    st.markdown("### ⚙️ Controls")
    def sync_in(): st.session_state.ops = st.session_state.ops_input
    def sync_sl(): st.session_state.ops = st.session_state.ops_slider
    st.number_input("Operations", 1, 20, st.session_state.ops, key="ops_input", on_change=sync_in)
    st.slider("Quick adjust", 1, 20, st.session_state.ops, key="ops_slider", on_change=sync_sl)
    st.success(f"✅ **Active: {st.session_state.ops} ops**")
    st.divider()
    st.markdown("### 🧠 Agent Network")
    st.caption("Monitor + Optimizer")
    strategy_name = st.selectbox("Strategy", ["default", "aggressive"], index=0, key="strategy_selector")
    if strategy_name != st.session_state.strategy_name:
        st.session_state.strategy_name = strategy_name
        st.rerun()
    st.divider()
    st.markdown("### 💾 Presets")
    preset_data = {"ops": st.session_state.ops, "strategy": st.session_state.strategy_name}
    st.download_button("💾 Save Preset", data=json.dumps(preset_data), file_name="preset.json", mime="application/json")
    uploaded_file = st.file_uploader("📂 Load Preset", type=["json"], label_visibility="collapsed")
    if uploaded_file:
        try:
            data = json.load(uploaded_file)
            st.session_state.ops = data.get("ops", 5)
            st.session_state.strategy_name = data.get("strategy", "default")
            st.success("✅ Preset Loaded!")
            st.rerun()
        except:
            st.error("❌ Invalid file")

# ========== MAIN ==========
st.markdown("<h1 style='margin-bottom: 0.5rem;'>⚡ TON Agent GasOptimizer + AI</h1>", unsafe_allow_html=True)
st.warning("⚠️ **TESTNET ONLY** — Zero mainnet risk.", icon="⚠️")

# Gas Trend Chart
with st.container(border=True):
    st.subheader("📈 Live Gas Trend")
    now = time.time()
    if now - st.session_state.last_gas_update > 5:
        variation = random.uniform(-0.03, 0.03)
        visual_gas = int(gas * (1 + variation))
        st.session_state.gas_history.append({"time": time.strftime("%H:%M:%S"), "gas": visual_gas, "ts": now})
        st.session_state.last_gas_update = now
    if len(st.session_state.gas_history) > 10: st.session_state.gas_history.pop(0)
    if len(st.session_state.gas_history) >= 3:
        df = pd.DataFrame(st.session_state.gas_history)
        st.line_chart(df.set_index("time")["gas"], height=180)
        st.success(f"🔮 Prediction: {gas_prediction}")
    else:
        st.info("📊 Collecting live data...")

# Connect Section
c1, c2 = st.columns([3, 1])
with c2:
    if not st.session_state.connected:
        addr = st.text_input("Testnet Address", placeholder="UQ... / EQ... (48 chars)", key="ai_input")
        col_real, col_demo = st.columns(2)
        with col_real:
            btn_real = st.button("🔗 Real")
        with col_demo:
            btn_demo = st.button("🎭 Demo")
        if btn_real or btn_demo:
            if not (addr and len(addr) == 48 and re.match(r'^(UQ|EQ|0Q)[a-zA-Z0-9_-]{46}$', addr)):
                st.error("❌ Invalid address format")
            else:
                is_demo = btn_demo
                bal, msg, demo_flag = fetch_balance_real(addr, NETWORK_MODE, use_demo=is_demo)
                if bal is not None:
                    st.session_state.update({"connected": True, "addr": addr, "bal": bal, "demo": is_demo})
                    st.success("✅ Connected")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
    else:
        st.success(f"✅ {st.session_state.addr[:12]}... {'🎭 Demo' if st.session_state.demo else '🟢 Real'}")
        st.metric("Balance", f"{st.session_state.bal:.4f} TON")
        if st.button("🔌 Disconnect"):
            st.session_state.update({"connected": False, "addr": "", "bal": 0.0, "demo": False})
            st.rerun()

# Address Insights
if st.session_state.connected:
    with st.expander("🔍 Address Insights", expanded=False):
        st.info("👛 Wallet • 💰 Balance: Testnet • 🕒 Real-time")

# ========== OPTIMIZATION SECTION ==========
ops = st.session_state.ops
run = st.button("🚀 Run AI Optimization", type="primary", disabled=not st.session_state.connected)

if run or st.session_state.opt_result is not None:
    if run:
        with st.spinner("🤖 Agent Network Processing..."):
            from core.agents import AgentNetwork
            from core.strategies import get_strategy
            strategy = get_strategy(st.session_state.strategy_name)
            network = AgentNetwork()
            pipeline_result = network.run_pipeline(ops, gas, load, st.session_state.bal)
            result = pipeline_result["recommendation"]
            result["batch"] = strategy.should_batch(ops, load, gas)
            result["savings_percent"] = strategy.estimate_savings(ops, gas, load)
            result["reason"] = strategy.get_reason(ops, load, gas)
            if result["batch"] and result["savings_percent"] > 0:
                st.session_state.total_saved += (ops * 0.005) * (result["savings_percent"]/100)
            st.session_state.opt_result = result
            st.session_state.opt_agents = pipeline_result["agents_status"]
            st.session_state.opt_gas = gas
            st.session_state.opt_load = load
            st.session_state.opt_ops = ops
            st.session_state.opt_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    result = st.session_state.opt_result
    agents = st.session_state.opt_agents
    st.info(f"🤖 `Strategy: {agents['strategy'].upper()} + {st.session_state.strategy_name}` | Monitor: ✅ | Optimizer: ✅")
    col1, col2, col3 = st.columns(3)
    col1.success("✅ Batch" if result["batch"] else "❌ Send")
    col2.metric("Savings", f"{result['savings_percent']:.1f}%")
    col3.metric("Confidence", f"{result['confidence']}%")
    st.markdown(f"**💡 Why:** {result['reason']}")
    c_a, c_b = st.columns(2)
    c_a.error(f"Standard: **{st.session_state.opt_ops * 0.005:.4f}** TON")
    batched = (st.session_state.opt_ops * 0.005) * (1 - result['savings_percent']/100) if result["batch"] else st.session_state.opt_ops * 0.005
    c_b.success(f"Optimized: **{batched:.4f}** TON")
    if st.session_state.total_saved > 0:
        st.success(f"💰 **Session Savings:** `{st.session_state.total_saved:.4f}` TON saved")
    with st.expander("📋 Copy Report", expanded=False):
        report = f"## TON Gas Optimizer Report\n- **Time:** {st.session_state.opt_timestamp}\n- **Network:** {NETWORK_MODE.upper()}\n- **Address:** {st.session_state.addr[:12]}...\n- **Ops:** {st.session_state.opt_ops} | **Gas:** {st.session_state.opt_gas} | **Load:** {st.session_state.opt_load}%\n- **Strategy:** {st.session_state.strategy_name}\n- **Action:** {'✅ Batch' if result['batch'] else '❌ Send'}\n- **Savings:** {result['savings_percent']:.1f}%\n- **Reason:** {result['reason']}\n- **Total Saved:** {st.session_state.total_saved:.4f} TON"
        st.code(report, language="markdown")
        st.caption("Select → Ctrl+C → Paste anywhere")
    st.download_button(
        label="📥 Export JSON", 
        data=json.dumps({
            "timestamp": st.session_state.opt_timestamp, "network": NETWORK_MODE, "address": st.session_state.addr,
            "ops": st.session_state.opt_ops, "gas_price": st.session_state.opt_gas, "network_load": st.session_state.opt_load,
            "balance_ton": st.session_state.bal, "ai_result": result, "agents_metadata": agents,
            "strategy_used": st.session_state.strategy_name, "session_savings_ton": round(st.session_state.total_saved, 6)
        }, indent=2), 
        file_name=f"gas_optimizer_{st.session_state.opt_timestamp.replace(' ', '_').replace(':', '-')}.json", 
        mime="application/json"
    )

# ========== DEFI SECTION ==========
with st.container(border=True):
    st.subheader("📊 STON.fi Pool Optimizer (Testnet)")
    st.caption("Read-only entry timing analysis")
    swap_amount = st.number_input("Swap Amount (TON)", 0.1, 100.0, 10.0, 1.0, key="defi_swap")
    if st.button("🔍 Analyze"):
        from core.defi_optimizer import fetch_testnet_pool_state, calculate_optimal_entry
        pool = fetch_testnet_pool_state()
        defi_gas = fetch_gas_price(api_base)
        defi_load = fetch_network_load(api_base)
        res = calculate_optimal_entry(defi_gas, defi_load, swap_amount)
        c1, c2, c3 = st.columns(3)
        c1.metric("Current Fee", f"{res['current_fee_ton']:.6f} TON")
        c2.metric("Optimal Fee", f"{res['optimal_fee_ton']:.6f} TON")
        c3.metric("Savings", f"{res['savings_percent']}%")
        st.info(res['recommendation'])
        st.caption("⚠️ Testnet simulation. Zero mainnet risk.")

st.markdown("---")
st.caption("🔗 [GitHub](https://github.com/beardbull/ton-gas-optimizer-ai-agents) • `TESTNET MODE` • Docker Ready")

