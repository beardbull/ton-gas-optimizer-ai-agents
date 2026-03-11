# demo/app.py - Smart simulation for reliable demo
# NOTE: In production, replace with real TON API calls
import streamlit as st
import json

st.set_page_config(page_title="TON Gas Optimizer AI", page_icon="⚡", layout="wide")

st.title("⚡ TON Agent GasOptimizer + Gemini AI")
st.markdown("""
**AI-powered gas optimization for TON blockchain agents**  
*Built for The Rise of AI Agents Hackathon • Lablab.ai*

> 💡 *Demo uses smart simulation. Production version connects to real TON network.*
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
        # AI decision logic
        should_batch = operations_count >= 3 and network_load < 80
        
        # SMART simulation based on realistic TON economics:
        # - Batching N ops costs ~1.3x single op (not N x 1.0)
        # - Higher network load = more congestion = more savings from batching
        # - Higher gas price = more $ saved by optimizing
        
        base_cost_per_op = 0.005  # TON
        
        if should_batch:
            # Realistic batching math
            separate_cost = operations_count * base_cost_per_op
            # Batched: first op full cost, rest discounted + overhead
            batched_cost = base_cost_per_op * (1 + 0.3 * (operations_count ** 0.5))
            
            # Load factor: more congestion = more savings
            load_factor = 1 + (network_load / 250)  # 1.0 to 1.4
            
            # Gas factor: higher price = more $ impact
            gas_factor = gas_price / 5000  # Normalize to base
            
            final_cost = batched_cost * load_factor * gas_factor
            savings_percent = max(0, (separate_cost - final_cost) / separate_cost * 100)
            optimized_cost = final_cost
        else:
            savings_percent = 0
            optimized_cost = operations_count * base_cost_per_op * (1 + network_load/250) * (gas_price/5000)
        
        base_cost = operations_count * base_cost_per_op * (1 + network_load/250) * (gas_price/5000)
        actual_savings = base_cost - optimized_cost
        
        st.success("✅ AI Decision Ready!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Should Batch?", "✅ Yes" if should_batch else "❌ No")
        with col2:
            st.metric("Estimated Savings", f"{savings_percent:.1f}%")
        with col3:
            st.metric("AI Confidence", f"{min(95, 70 + operations_count * 2)}%")
        
        reason = f"{operations_count} ops • {network_load}% load • {gas_price} nanoTON"
        st.info(f"🧠 **Decision factors:** {reason}")
        
        st.markdown("---")
        st.markdown("### 💰 Cost Comparison")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.error(f"❌ Without batching: {base_cost:.4f} TON")
        with col_b:
            st.success(f"✅ With AI batching: {optimized_cost:.4f} TON")
        
        if should_batch and actual_savings > 0:
            st.markdown(f"**💵 You save:** `{actual_savings:.4f} TON` (~${actual_savings * 0.5:.4f} USD)")
            st.caption("💡 Savings scale with network conditions")

# Footer with honest note
st.markdown("---")
st.caption("""
🔗 [GitHub Repo](https://github.com/beardbull/ton-gas-optimizer-ai-agents)  
*Demo uses smart simulation • Production: real TON API + Gemini AI*
""")
