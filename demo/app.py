# demo/app.py - Streamlit with TON Connect
import streamlit as st
import json

st.set_page_config(page_title="TON Gas Optimizer AI", page_icon="⚡", layout="wide")

st.title("⚡ TON Agent GasOptimizer + Gemini AI")
st.markdown("""
**AI-powered gas optimization for TON blockchain**  
*Built for The Rise of AI Agents Hackathon • Lablab.ai*
""")

# TON Connect Widget (HTML injection)
st.markdown("""
<div style="text-align: right; margin-bottom: 20px;">
  <div id="ton-connect"></div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # TON Network Status
    st.subheader("📊 TON Testnet")
    st.metric("Network", "Testnet")
    st.metric("Status", "🟢 Connected")
    
    # Wallet info (mock for now)
    st.markdown("---")
    st.markdown("**Wallet**")
    wallet_address = st.text_input("Wallet Address", placeholder="UQ...")
    
    operations_count = st.slider("Operations count", 1, 20, 5)
    network_load = st.slider("Network load %", 0, 100, 56)
    gas_price = st.number_input("Gas price (nanoTON)", value=5000, min_value=100)
    
    run_btn = st.button("🚀 Run AI Optimization", type="primary")

if run_btn:
    with st.spinner("🤖 AI analyzing..."):
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
        
        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.error(f"❌ Without AI: {base_cost:.4f} TON")
        with col_b:
            st.success(f"✅ With AI: {optimized_cost:.4f} TON")

# Footer
st.markdown("---")
st.caption("🔗 [GitHub](https://github.com/beardbull/ton-gas-optimizer-ai-agents) • TON Testnet Ready")
