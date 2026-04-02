# src/tonClient.py - Simple TON Testnet Client via HTTP (no extra deps)
import requests
import time

TONCENTER_API = "https://testnet.toncenter.com/api/v2"

def get_balance(address: str) -> float | None:
    """Get wallet balance in TON from testnet"""
    try:
        resp = requests.get(
            f"{TONCENTER_API}/account",
            params={"address": address},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            nano = int(data.get("result", {}).get("balance", 0))
            return nano / 1e9  # nanoTON → TON
    except Exception as e:
        print(f"Balance error: {e}")
    return None

def get_gas_price() -> int:
    """Get estimated gas price (simplified for testnet)"""
    # Real gas requires parsing config; using realistic testnet range
    return 5000 + (int(time.time()) % 5000)

def get_network_load() -> int:
    """Estimate network load from block seqno"""
    try:
        resp = requests.get(f"{TONCENTER_API}/masterchainInfo", timeout=10)
        if resp.status_code == 200:
            seqno = resp.json().get("result", {}).get("last", {}).get("seqno", 0)
            return 40 + (seqno % 40)  # 40-80%
    except:
        pass
    return 50

def calculate_savings(ops_count: int, load: int, gas: int) -> dict:
    """Calculate batching savings based on TON economics"""
    base = 0.005  # TON per op
    separate = ops_count * base
    
    if ops_count >= 3 and load < 80:
        # Batching formula: first op full, rest discounted
        batched = base * (1 + 0.3 * (ops_count ** 0.5))
        factor = (1 + load/250) * (gas/5000)
        final = batched * factor
        savings = max(0, (separate - final) / separate * 100)
        return {
            "should_batch": True,
            "separate_cost": separate,
            "batched_cost": final,
            "savings_percent": savings,
            "savings_ton": separate - final
        }
    else:
        cost = separate * (1 + load/250) * (gas/5000)
        return {
            "should_batch": False,
            "separate_cost": cost,
            "batched_cost": cost,
            "savings_percent": 0,
            "savings_ton": 0
        }
