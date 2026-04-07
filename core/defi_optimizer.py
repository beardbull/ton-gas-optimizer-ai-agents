import random
from typing import Dict

class DeFiOptimizer:
    """
    Анализ оптимальных маршрутов для DeFi-свопов в сети TON.
    Сравнивает Direct vs Multi-hop, оценивает slippage, DEX-fee и gas cost.
    """
    def __init__(self):
        self.pools = {
            "TON/USDT": {"liquidity": 8_500_000, "fee_tier": 0.0030, "volatility": 0.0001},
            "TON/NOT":  {"liquidity": 12_000_000, "fee_tier": 0.0030, "volatility": 0.00015},
            "TON/DOGS": {"liquidity": 6_200_000, "fee_tier": 0.0035, "volatility": 0.00025},
            "TON/STON": {"liquidity": 4_800_000, "fee_tier": 0.0030, "volatility": 0.00012}
        }

    def analyze_swap(self, amount_ton: float, pair: str, slippage_tol: float = 0.5) -> Dict:
        if pair not in self.pools:
            return {"error": "Pool not found"}

        pool = self.pools[pair]
        
        # 1. Оценка влияния на цену (Price Impact)
        price_impact = (amount_ton / pool["liquidity"]) * pool["volatility"] * 100
        
        # 2. Комиссия DEX
        dex_fee = amount_ton * pool["fee_tier"]
        
        # 3. Стоимость газа (зависит от нагрузки)
        gas_cost = 0.005 + random.uniform(0.001, 0.004)
        
        # 4. Анализ маршрутов
        # Direct: 1 транзакция
        direct_output = amount_ton - dex_fee - gas_cost
        direct_route = f"Direct: {pair}"
        
        # Multi-hop: 2 транзакции (выгодно при больших объёмах)
        multi_hop_threshold = 50.0
        if amount_ton > multi_hop_threshold and random.random() > 0.5:
            # Симуляция разбиения через пул ликвидности
            split_fee = amount_ton * 0.0025  # Чуть ниже за счёт объема
            split_gas = gas_cost * 1.35      # Дороже газ (2 tx)
            multi_hop_output = amount_ton - split_fee - split_gas
            
            if multi_hop_output > direct_output:
                output = multi_hop_output
                route = "Multi-Hop (через STON.fi/DeDust)"
                savings_vs_direct = multi_hop_output - direct_output
            else:
                output = direct_output
                route = direct_route
                savings_vs_direct = 0.0
        else:
            output = direct_output
            route = direct_route
            savings_vs_direct = 0.0

        # 5. Рекомендации
        rec_status = "✅ Route optimal. Execute now."
        timing = "Execute now"
        
        if price_impact > slippage_tol:
            rec_status = "⚠️ High slippage. Split into smaller batches."
            timing = "Wait for higher liquidity"
        if gas_cost > 0.008:
            rec_status = "⛽ High gas. Wait for network cooldown."
            timing = "Wait for lower gas"
            
        return {
            "pair": pair,
            "input_amount": amount_ton,
            "estimated_output": round(output, 4),
            "dex_fee": round(dex_fee, 4),
            "gas_cost": round(gas_cost, 4),
            "price_impact": round(price_impact, 2),
            "route": route,
            "savings_vs_direct": round(savings_vs_direct, 4),
            "recommendation": rec_status,
            "timing": timing
        }
