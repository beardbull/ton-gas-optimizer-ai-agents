# ⚡ TON Agent GasOptimizer + Gemini AI

![Project Cover](assets/cover.png)

> **Submitted to:** [The Rise of AI Agents Hackathon](https://lablab.ai/event/the-rise-of-ai-agents-hackathon) • Lablab.ai

**AI-powered gas optimization for TON blockchain agents**

🔗 **Live Demo:** https://ton-gas-optimizer-ai-agents-....streamlit.app  
🔗 **GitHub:** https://github.com/beardbull/ton-gas-optimizer-ai-agents

---

## 🎯 Problem
AI agents execute many small transactions → high gas costs on TON.

## 💡 Solution
- **Batching**: combine operations → ~70% gas savings
- **AI Decision**: Algorithm analyzes network conditions (gas price, load) to recommend batching
- **MCP-compatible**: easy integration into any AI agent

---

## 📊 Current Status

| Feature | Status | Source |
|---------|--------|--------|
| 📈 Gas Price | ✅ Real-time | toncenter API v2 |
| 🌐 Network Load | ✅ Real-time | toncenter API v2 |
| 💰 Wallet Balance | ✅ Real-time | tonapi.io v2 |
| 🧠 AI Optimization | ✅ Working | Core logic |
| 🔗 Network Switch | ✅ In UI | Testnet/Mainnet toggle |
| 🔗 Connect Mode | ✅ Real / Demo | Two buttons |

---

## 🛠️ Built With
- TON Blockchain
- Streamlit (Python)
- toncenter API v2
- tonapi.io v2
- MCP-compatible architecture

---

## 🧪 Data Sources

| Data | API Endpoint | Status |
|------|-------------|--------|
| Balance | tonapi.io/v2/accounts/{address} | ✅ Working |
| Gas Price | toncenter.com/api/v2/getConfig?id=21 | ✅ Working |
| Network Load | toncenter.com/api/v2/masterchainInfo | ✅ Working |

> **Note:** Balance values may vary slightly across explorers due to indexing latency. This is normal for TON testnet.

---

## 🚀 How to Use
1. Open: https://ton-gas-optimizer-ai-agents-....streamlit.app
2. Select Network in sidebar (🧪 Testnet or 🌐 Mainnet)
3. Enter valid TON address (48 chars, starts with UQ/EQ/0Q)
4. Click 🔗 Real (fetch from API) or 🎭 Demo (deterministic)
5. Click "🚀 Run AI Optimization" to see batching recommendation

---

## 🔧 Local Development
```bash
git clone https://github.com/beardbull/ton-gas-optimizer-ai-agents
cd ton-gas-optimizer-ai-agents
pip install -r requirements.txt
streamlit run demo/app.py