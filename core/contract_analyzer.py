import re
from typing import Dict, List

class ContractAnalyzer:
    """
    Агент анализа сложности смарт-контрактов (FunC/Fift псевдо-парсер).
    Оценивает вычислительную стоимость на основе паттернов кода.
    Работает локально, без внешних API.
    """
    def __init__(self):
        self.patterns = {
            "loops": [r"\b(for|while|repeat)\b", r"\<\[\]"],
            "storage_write": [r"set_data", r"dict_set", r"c4@", r"storage_set"],
            "crypto_ops": [r"hash_sha256", r"check_sign", r"curve25519", r"prng"],
            "external_calls": [r"send_msg", r"raw_reserve", r"bounce", r"accept_message"],
            "heavy_math": [r"muldiv", r"pow", r"sqrt", r"log"]
        }
        self.weights = {
            "loops": 40,
            "storage_write": 35,
            "crypto_ops": 20,
            "external_calls": 15,
            "heavy_math": 10
        }

    def analyze(self, code_snippet: str) -> Dict:
        if not code_snippet or len(code_snippet.strip()) < 10:
            return {"error": "Empty or invalid code snippet"}

        score = 0
        detected_patterns: List[Dict] = []
        recommendations: List[str] = []

        for category, regex_list in self.patterns.items():
            weight = self.weights[category]
            for pattern in regex_list:
                matches = re.findall(pattern, code_snippet, re.IGNORECASE)
                if matches:
                    count = len(matches)
                    category_score = min(weight * count, weight * 3)  # Cap at 3x
                    score += category_score
                    detected_patterns.append({
                        "category": category,
                        "count": count,
                        "risk_score": category_score,
                        "examples": matches[:3]
                    })

        # Нормализация и уровень
        max_score = 150
        normalized = min(score / max_score, 1.0)
        
        if normalized < 0.3: level = "LOW"
        elif normalized < 0.7: level = "MEDIUM"
        else: level = "HIGH"

        # Рекомендации
        if "loops" in [p["category"] for p in detected_patterns]:
            recommendations.append("⚠️ Избегайте динамических циклов. Используйте фиксированные итерации.")
        if "storage_write" in [p["category"] for p in detected_patterns]:
            recommendations.append("💾 Оптимизируйте запись в хранилище. Группируйте данные.")
        if normalized > 0.7:
            recommendations.append("🔥 Высокая сложность! Рассмотрите батчинг или off-chain вычисления.")
        if not recommendations:
            recommendations.append("✅ Контракт оптимален. Стандартные gas-лимиты подойдут.")

        # Оценка газа (mock на основе сложности)
        base_gas = 5000
        estimated_gas = int(base_gas + (normalized * 15000))

        return {
            "complexity_level": level,
            "score": round(normalized * 100, 1),
            "estimated_gas_nano": estimated_gas,
            "patterns_detected": detected_patterns,
            "recommendations": recommendations,
            "safe_to_batch": level != "HIGH"
        }
