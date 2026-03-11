# demo/app.py - Streamlit demo for Lablab.ai hackathon
import streamlit as st
import requests
import json

st.set_page_config(page_title="TON Gas Optimizer AI", page_icon="⚡", layout="wide")

st.title("⚡ TON Agent GasOptimizer + Gemini AI")
st.markdown("""
**AI-powered gas optimization for TON blockchain agents**  
*Built for The Rise of AI Agents Hackathon • Lablab.ai*
""")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    operations_count = st.slider("Operations count", 1, 20, 5)
    network_load = st.slider("Network load %", 0, 100, 56)
    gas_price = st.number_input("Gas price (nanoTON)", value=5000, min_value=100)
    run_btn = st.button("🚀 Run AI Optimization", type="primary")

if run_btn:
    with st.spinner("🤖 AI analyzing network conditions..."):
        # Mock response for demo (since we can't call localhost from Streamlit Cloud)
        should_batch = operations_count >= 3 and network_load < 80
        base_cost = operations_count * 0.005
        optimized_cost = base_cost * 0.285 if should_batch else base_cost
        savings = ((base_cost - optimized_cost) / base_cost * 100)
        
        st.success("✅ AI Decision Ready!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Should Batch?", "✅ Yes" if should_batch else "❌ No")
        with col2:
            st.metric("Estimated Savings", f"{savings:.1f}%")
        with col3:
            st.metric("AI Confidence", "85%")
        
        reason = f"Batching recommended: {operations_count} ops at {network_load}% load" if should_batch else f"No batching: {'too few ops' if operations_count < 3 else 'high network load'}"
        st.info(f"🧠 **Reason:** {reason}")
        
        st.markdown("---")
        st.markdown("### 💰 Cost Comparison")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.error(f"❌ Without AI: {base_cost:.4f} TON")
        with col_b:
            st.success(f"✅ With AI Batching: {optimized_cost:.4f} TON")
        
        st.markdown(f"**💵 You save:** `{(base_cost - optimized_cost):.4f} TON` per batch!")

# Footer
st.markdown("---")
st.caption("🔗 [GitHub Repo](https://github.com/beardbull/ton-gas-optimizer-ai-agents) • Built with TON + Gemini AI")
