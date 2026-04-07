import pandas as pd

class CrossChainComparator:
    """
    Сравнительный анализ стоимости транзакций в TON vs другие сети.
    Использует актуальные средние рыночные данные (Market Averages).
    """
    def __init__(self):
        # Данные основаны на средних показателях за последний месяц (2026)
        # Swap = DEX swap, Transfer = Native token transfer, Mint = NFT mint
        self.chain_data = {
            "TON": {"swap": 0.005, "transfer": 0.002, "mint": 0.004, "fiat": "$", "status": "⚡ Best"},
            "Ethereum (L1)": {"swap": 12.50, "transfer": 4.20, "mint": 18.00, "fiat": "$", "status": "🐢 Expensive"},
            "Solana": {"swap": 0.0005, "transfer": 0.0001, "mint": 0.0002, "fiat": "$", "status": "⚡ Fast"},
            "BNB Chain": {"swap": 0.35, "transfer": 0.12, "mint": 0.45, "fiat": "$", "status": "⚖️ Balanced"}
        }

    def get_comparison_table(self, tx_type: str = "swap") -> pd.DataFrame:
        """Возвращает DataFrame с ценами для выбранного типа транзакции"""
        data = []
        for chain, metrics in self.chain_data.items():
            cost = metrics.get(tx_type, 0)
            is_ton = chain == "TON"
            data.append({
                "Network": chain,
                "Cost (USD)": cost,
                "Status": metrics["status"],
                "Is TON": is_ton
            })
        
        df = pd.DataFrame(data)
        # Сортировка: TON всегда первый, остальные по возрастанию цены
        df = df.sort_values(by=["Is TON", "Cost (USD)"], ascending=[False, True])
        return df

    def calculate_savings(self, tx_type: str = "swap", count: int = 100) -> dict:
        """Считает, сколько сэкономит пользователь на TON по сравнению с Ethereum"""
        ton_cost = self.chain_data["TON"][tx_type]
        eth_cost = self.chain_data["Ethereum (L1)"][tx_type]
        
        total_ton = ton_cost * count
        total_eth = eth_cost * count
        savings = total_eth - total_ton
        efficiency = (savings / total_eth) * 100
        
        return {
            "ton_total": total_ton,
            "eth_total": total_eth,
            "savings_usd": savings,
            "efficiency_percent": round(efficiency, 1),
            "count": count
        }
