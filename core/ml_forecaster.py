import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict, List

class GasForecaster:
    """
    Модуль машинного обучения для прогнозирования тренда газа.
    Использует Linear Regression для анализа временных рядов.
    """
    def __init__(self):
        self.model = LinearRegression()
        self.min_data_points = 5

    def predict_trend(self, gas_history: List[float]) -> Dict:
        """
        Принимает список цен газа [5000, 5100, 4900, ...]
        Возвращает прогноз тренда.
        """
        if not gas_history or len(gas_history) < self.min_data_points:
            return {
                "trend": "UNKNOWN",
                "signal": "INSUFFICIENT_DATA",
                "confidence": 0,
                "message": "Нужно минимум 5 точек данных для анализа"
            }

        # Подготовка данных для ML
        # X - индексы времени (0, 1, 2...), y - цена газа
        X = np.array(range(len(gas_history))).reshape(-1, 1)
        y = np.array(gas_history)

        try:
            # Обучение модели
            self.model.fit(X, y)

            # Прогноз на следующий шаг
            next_index = np.array([[len(gas_history)]])
            predicted_value = self.model.predict(next_index)[0]

            # Анализ угла наклона (коэффициент k)
            slope = self.model.coef_[0]

            # Интерпретация тренда
            signal = "HOLD"
            if slope > 30:
                signal = "BATCH_NOW" # Газ растет, батчим сейчас
            elif slope < -30:
                signal = "WAIT"      # Газ падает, ждем

            # Оценка уверенности (R^2 score)
            confidence = self.model.score(X, y)
            
            return {
                "trend": "UP" if slope > 0 else "DOWN",
                "signal": signal,
                "predicted_gas": round(predicted_value, 0),
                "confidence": round(confidence * 100, 1),
                "slope": round(slope, 2)
            }
        except Exception as e:
            return {"error": str(e)}

    def generate_recommendation(self, prediction: Dict) -> str:
        if prediction.get("error"): return "⚠️ Ошибка ML"
        
        conf = prediction["confidence"]
        sig = prediction["signal"]
        
        # Логика рекомендаций
        if sig == "BATCH_NOW" and conf > 60:
            return "🚀 ГАЗ РАСТЁТ! Срочно батчьте транзакции!"
        elif sig == "WAIT" and conf > 60:
            return "⏳ Газ падает. Лучше подождать."
        else:
            return "➡️ Ситуация стабильная. Действуйте по плану."
