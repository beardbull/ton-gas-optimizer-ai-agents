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
• **Batching**: combine operations → **~70% gas savings**  
• **AI Decision**: Algorithm analyzes network conditions (gas price, load) to recommend batching  
• **MCP-compatible**: easy integration into any AI agent

---

## 📊 Current Status

| Feature | Status | Details |
|---------|--------|---------|
| 📈 Gas Price | ✅ **Real-time** | Fetched from toncenter API v2 (`/getConfig`) |
| 🌐 Network Load | ✅ **Real-time** | Fetched from toncenter API v2 (`/masterchainInfo`) |
| 💰 Wallet Balance | ⚠️ Deterministic | API `/account` endpoint currently unavailable; uses hash-based fallback (same address = same value) |
| 🧠 AI Optimization | ✅ **Fully Working** | Core logic is network-agnostic and fully testable |
| 🔗 Network Switch | ✅ In UI | Toggle between Testnet/Mainnet in sidebar |

---

## 🛠️ Built With
- **Blockchain**: TON (The Open Network)
- **AI**: Algorithmic optimization (Gemini-ready architecture)
- **Frontend**: Streamlit (Python)
- **API**: toncenter.com API v2
- **Integration**: MCP-compatible design

---

## 🔮 Architecture
