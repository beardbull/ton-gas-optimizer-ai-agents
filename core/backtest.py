import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, Callable

class GasBacktester:
    """
    Модуль бэктестинга стратегий оптимизации газа.
    Позволяет прогонять стратегии на исторических данных, 
    рассчитывать накопленную экономию и формировать отчёты.
    """
    def __init__(self, base_gas: float = 5000.0, base_tx_cost_ton: float = 0.005):
        self.base_gas = base_gas
        self.base_tx_cost_ton = base_tx_cost_ton

    def generate_mock_history(self, days: int = 7, intervals_per_day: int = 24) -> pd.DataFrame:
        """Генерирует синтетическую историю газа для тестирования стратегий"""
        records = []
        now = datetime.now()
        total_points = days * intervals_per_day

        for i in range(total_points):
            ts = now - timedelta(hours=(total_points - i))
            # Симуляция волатильности: базовый уровень + синусоидальный тренд + шум
            trend = 500 * np.sin(i / 10)
            noise = np.random.normal(0, 300)
            gas_price = max(1000, self.base_gas + trend + noise)
            records.append({"timestamp": ts, "gas_price": gas_price})

        return pd.DataFrame(records)

    def simulate_strategy(self, df: pd.DataFrame, strategy_fn: Callable[[int, float, float], bool], ops_per_interval: int = 5) -> pd.DataFrame:
        """
        Прогоняет стратегию по истории.
        strategy_fn: функция вида should_batch(ops, load, gas) -> bool
        """
        results = []
        
        for _, row in df.iterrows():
            gas = row["gas_price"]
            load = random.uniform(20, 90)  # Симуляция сетевой нагрузки

            # Базовая стоимость (без оптимизации): N операций = N транзакций
            interval_standard = ops_per_interval * self.base_tx_cost_ton * (gas / self.base_gas)

            # Оптимизированная стоимость
            should_batch = strategy_fn(ops_per_interval, load, gas)
            if should_batch:
                # Батчинг: 1 транзакция вместо N, с коэффициентом сложности 1.2
                interval_optimized = 1 * self.base_tx_cost_ton * (gas / self.base_gas) * 1.2
            else:
                interval_optimized = interval_standard

            savings = max(0, (interval_standard - interval_optimized) / interval_standard * 100)

            results.append({
                "timestamp": row["timestamp"],
                "gas_price": gas,
                "standard_cost": interval_standard,
                "optimized_cost": interval_optimized,
                "savings_percent": round(savings, 2),
                "action": "BATCH" if should_batch else "SEND"
            })

        res_df = pd.DataFrame(results)
        res_df["cumulative_savings_ton"] = (res_df["standard_cost"] - res_df["optimized_cost"]).cumsum()
        return res_df

    def get_summary(self, result_df: pd.DataFrame) -> Dict:
        """Формирует сводную статистику по результатам бэктеста"""
        total_standard = result_df["standard_cost"].sum()
        total_optimized = result_df["optimized_cost"].sum()
        return {
            "total_standard_ton": round(total_standard, 4),
            "total_optimized_ton": round(total_optimized, 4),
            "total_saved_ton": round(total_standard - total_optimized, 4),
            "avg_savings_percent": round(result_df["savings_percent"].mean(), 1),
            "batch_count": int((result_df["action"] == "BATCH").sum()),
            "send_count": int((result_df["action"] == "SEND").sum()),
            "total_intervals": len(result_df)
        }
