cd "C:\Users\Wakky\Desktop\The Rise of AI Agents Hackathon (Lablab.ai)\ton-gas-optimizer-The Rise of AI Agents"

@'
# config.py - Network configuration for TON Gas Optimizer

# NETWORK: "testnet" or "mainnet"
# Change this to switch between networks
NETWORK = "mainnet"  # ← МЕНЯЙ ЗДЕСЬ: "testnet" или "mainnet"

# LOCAL_DEV: True = use localhost mock server, False = use real API
LOCAL_DEV = False

# API endpoints based on NETWORK
if NETWORK == "testnet":
    API_BASE = "https://testnet.toncenter.com/api/v2"
    EXPLORER_BASE = "https://testnet.tonscan.org"
else:  # mainnet
    API_BASE = "https://toncenter.com/api/v2"
    EXPLORER_BASE = "https://tonscan.org"

# Mock server endpoint (for LOCAL_DEV = True)
MOCK_API_BASE = "http://localhost:8080/api/v2"
'@ | Out-File -FilePath "config.py" -Encoding utf8

echo "✅ config.py создан"
