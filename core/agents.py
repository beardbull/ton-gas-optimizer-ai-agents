# core/agents.py - Lightweight 2-Agent Architecture
import time
from typing import Dict, Any

class MonitorAgent:
    def __init__(self): self.status = "idle"
    def fetch_conditions(self, gas: int, load: int) -> Dict[str, Any]:
        self.status = "scanning"
        conditions = {"gas_nano": gas, "load_percent": load, "timestamp": time.time(),
                     "threshold_met": gas < 3000 and load < 80,
                     "gas_label": "low" if gas < 3000 else "normal" if gas < 5000 else "high"}
        self.status = "ready"
        return conditions

class OptimizerAgent:
    def __init__(self): self.status = "idle"; self.strategy_used = "rule-based"
    def analyze(self, conditions: Dict[str, Any], ops: int, balance_ton: float) -> Dict[str, Any]:
        self.status = "computing"
        gas, load = conditions["gas_nano"], conditions["load_percent"]
        should_batch = ops >= 3 and load < 80
        base_savings = 25 if should_batch else 0
        reason = f"Network load: {load}%, Gas: {conditions['gas_label']}"
        try:
            from core.ai_engine import get_ai_recommendation
            ai_result = get_ai_recommendation(ops, load, gas, balance_ton)
            if ai_result.get("confidence", 0) > 75:
                result = ai_result; result["reason"] = reason; self.strategy_used = "ai-enhanced"
            else: raise ValueError("Low AI confidence")
        except:
            result = {"batch": should_batch, "reason": reason, "savings_percent": base_savings,
                     "confidence": 80, "alternative_action": "Wait for load < 80%" if load >= 80 else "",
                     "source": "Rule-based fallback"}
            self.strategy_used = "rule-based"
        result["gas_condition"] = conditions["gas_label"]
        self.status = "completed"
        return result

class AgentNetwork:
    def __init__(self): self.monitor = MonitorAgent(); self.optimizer = OptimizerAgent(); self.status = "initialized"
    def run_pipeline(self, ops: int, gas: int, load: int, balance_ton: float) -> Dict[str, Any]:
        self.status = "active"
        conditions = self.monitor.fetch_conditions(gas, load)
        recommendation = self.optimizer.analyze(conditions, ops, balance_ton)
        self.status = "completed"
        return {"agents_status": {"monitor": self.monitor.status, "optimizer": self.optimizer.status,
                "strategy": self.optimizer.strategy_used}, "conditions": conditions, "recommendation": recommendation}
