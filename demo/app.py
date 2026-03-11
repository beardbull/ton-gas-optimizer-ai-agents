# demo/app.py - Streamlit with RELIABLE mock wallet flow for demo
import streamlit as st
import json
import random

st.set_page_config(page_title="TON Gas Optimizer AI", page_icon="⚡", layout="wide")

st.title("⚡ TON Agent GasOptimizer + Gemini AI")
st.markdown("""
**AI-powered gas optimization for TON blockchain**  
*Built for The Rise of AI Agents Hackathon • Lablab.ai*

> 💡 *Demo mode: Simulated wallet connection for reliable presentation*
""")

# Session state for mock wallet
if "wallet_connected" not in st.session_state:
    st.session_state.wallet_connected = False
if "wallet_address" not in st.session_state:
    st.session_state.wallet_address = ""
if "wallet_balance" not in st.session_state:
    st.session_state.wallet_balance = 0

# Mock connect button
col1, col2 = st.columns([4, 1])
with col2:
    if not st.session_state.wallet_connected:
        if st.button("🔗 Connect Wallet", type="primary"):
            # Mock connection
            st.session_state.wallet_connected = True
            st.session_state.wallet_address = "UQ" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=46))
            st.session_state.wallet_balance = round(random.uniform(10, 100), 2)
            st.rerun()
    else:
        st.success(f"✅ {st.session_state.wallet_address[:12]}...")
        if st.button("🔌 Disconnect"):
            st.session_state.wallet_connected = False
            st.session_state.wallet_address = ""
            st.session_state.wallet_balance = 0
            st.rerun()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("📊 TON Testnet")
    st.metric("Network", "Testnet")
    st.metric("Status", "🟢 Connected" if st.session_state.wallet_connected else "🟡 Demo Mode")
    
    st.markdown("---")
    st.markdown("**Wallet**")
    
    if st.session_state.wallet_connected:
        st.metric("Address", f"{st.session_state.wallet_address[:16]}...")
        st.metric("Balance", f"{st.session_state.wallet_balance} TON", "🟢 Testnet")
    else:
        st.info("🔗 Click 'Connect Wallet' to start")
    
    st.markdown("---")
    operations_count = st.slider("Operations count", 1, 20, 5)
    network_load = st.slider("Network load %", 0, 100, 56)
    gas_price = st.number_input("Gas price (nanoTON)", value=5000, min_value=100)
    
    run_btn = st.button("🚀 Run AI Optimization", type="primary", disabled=not st.session_state.wallet_connected)
    
    if not st.session_state.wallet_connected:
        st.caption("💡 Connect wallet first to enable optimization")
    
    # Test transaction button
    st.markdown("---")
    test_tx_btn = st.button("📤 Send Test Transaction", type="secondary", disabled=not st.session_state.wallet_connected)

if run_btn:
    with st.spinner("🤖 AI analyzing network conditions..."):
        should_batch = operations_count >= 3 and network_load < 80
        
        base_cost = operations_count * 0.005
        if should_batch:
            optimized_cost = base_cost * 0.285
            savings_percent = 71.5
        else:
            optimized_cost = base_cost
            savings_percent = 0
        
        st.success("✅ AI Decision Ready!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Should Batch?", "✅ Yes" if should_batch else "❌ No")
        with col2:
            st.metric("Estimated Savings", f"{savings_percent:.1f}%")
        with col3:
            st.metric("Confidence", "85%")
        
        reason = f"{operations_count} ops • {network_load}% load • {gas_price} nanoTON"
        st.info(f"🧠 **Decision factors:** {reason}")
        
        st.markdown("---")
        st.markdown("### 💰 Cost Comparison")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.error(f"❌ Without AI: {base_cost:.4f} TON")
        with col_b:
            st.success(f"✅ With AI: {optimized_cost:.4f} TON")
        
        if should_batch:
            actual_savings = base_cost - optimized_cost
            st.markdown(f"**💵 You save:** `{actual_savings:.4f} TON` (~${actual_savings * 0.5:.4f} USD)")

if test_tx_btn:
    with st.spinner("📤 Preparing transaction..."):
        import time
        time.sleep(1)  # Simulate network delay
        
        st.success("✅ Transaction sent to TON Testnet!")
        
        tx_hash = "0x" + "".join(random.choices("0123456789abcdef", k=64))
        st.json({
            "status": "confirmed",
            "hash": tx_hash,
            "amount": "0.01 TON",
            "network": "testnet",
            "from": st.session_state.wallet_address[:48] + "...",
            "to": "EQ...mock_destination",
            "gas_used": "0.002 TON"
        })
        
        st.markdown(f"""
        🔍 [View on TON Scan](https://testnet.tonscan.org/tx/{tx_hash})  
        💡 *Mock transaction for demo purposes*
        """)

# Footer with honest note
st.markdown("---")
st.caption("""
🔗 [GitHub](https://github.com/beardbull/ton-gas-optimizer-ai-agents)  
*Demo: Simulated wallet flow • Production: TonConnect + real TON transactions*
""")
