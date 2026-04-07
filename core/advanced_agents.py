import random
from typing import Dict

class RiskAgent:
    """
    Агент оценки рисков.
    Анализирует баланс, стоимость транзакции и загрузку сети.
    """
    def evaluate(self, balance_ton: float, estimated_cost_ton: float, network_load_pct: int) -> Dict:
        risk_score = 0.0
        reasons = []
        
        # Проверка 1: Достаточно ли запаса по балансу (минимум 1.5x от стоимости)
        if balance_ton < estimated_cost_ton * 1.5:
            risk_score += 0.5
            reasons.append("Low balance buffer (<1.5x cost)")
            
        # Проверка 2: Перегруженность сети
        if network_load_pct > 80:
            risk_score += 0.3
            reasons.append("High network congestion (>80%)")
        elif network_load_pct > 60:
            risk_score += 0.1
            reasons.append("Moderate network load")
            
        # Проверка 3: Симуляция случайных сетевых флуктуаций
        risk_score += random.uniform(0, 0.1)
        
        # Нормализация
        risk_score = min(risk_score, 1.0)
        
        # Определение уровня риска
        risk_level = "LOW"
        if risk_score > 0.4: risk_level = "MEDIUM"
        if risk_score > 0.7: risk_level = "HIGH"
        
        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "reasons": reasons,
            "safe_to_send": risk_level != "HIGH"
        }

class ContractAnalyzer:
    """
    Агент анализа контракта.
    Оценивает вычислительную сложность и стоимость газа (Compute cost).
    """
    def analyze(self, ops_count: int, is_complex_logic: bool = False) -> Dict:
        # Базовая стоимость одной операции в TON (приблизительно)
        base_cost_ton = 0.0005
        
        # Множитель сложности (например, циклы внутри контракта)
        multiplier = 1.8 if is_complex_logic else 1.0
        
        # Расчет общей стоимости
        estimated_cost = ops_count * base_cost_ton * multiplier
        
        # Рекомендуемый лимит газа (в NanoTON)
        # 1 TON = 10^9 NanoTON. Умножаем на 2,000,000 для получения NanoTON для газа
        recommended_gas = int(estimated_cost * 2_000_000)
        
        return {
            "estimated_cost_ton": round(estimated_cost, 4),
            "complexity_level": "HIGH" if is_complex_logic else "STANDARD",
            "recommended_gas_nano": recommended_gas,
            "analysis_note": "Complex logic detected" if is_complex_logic else "Standard operations"
        }
