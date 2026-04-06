# core/strategies.py - Plugin-ready Strategy Interface
from abc import ABC, abstractmethod
from typing import Dict, Any

class OptimizationStrategy(ABC):
    @abstractmethod
    def should_batch(self, ops: int, load: int, gas: int) -> bool: pass
    @abstractmethod
    def estimate_savings(self, ops: int, gas: int, load: int) -> float: pass
    @abstractmethod
    def get_reason(self, ops: int, load: int, gas: int) -> str: pass

class DefaultStrategy(OptimizationStrategy):
    def should_batch(self, ops: int, load: int, gas: int) -> bool: return ops >= 3 and load < 80
    def estimate_savings(self, ops: int, gas: int, load: int) -> float:
        return 25.0 + min(20.0, (80 - load) * 0.25) if self.should_batch(ops, load, gas) else 0.0
    def get_reason(self, ops: int, load: int, gas: int) -> str:
        if load >= 80: return f"High network load ({load}%) — batching may delay confirmation"
        if ops < 3: return f"Low operation count ({ops}) — batching overhead not justified"
        gas_label = "low" if gas < 3000 else "normal" if gas < 5000 else "high"
        return f"Optimal conditions: {ops} ops, {gas_label} gas ({gas} nano), load {load}%"

class AggressiveStrategy(OptimizationStrategy):
    def should_batch(self, ops: int, load: int, gas: int) -> bool: return ops >= 2 and load < 90
    def estimate_savings(self, ops: int, gas: int, load: int) -> float:
        return 15.0 + min(30.0, (90 - load) * 0.33) if self.should_batch(ops, load, gas) else 0.0
    def get_reason(self, ops: int, load: int, gas: int) -> str:
        return f"Aggressive mode: batching {ops} ops at {load}% load for max throughput"

def get_strategy(name: str = "default") -> OptimizationStrategy:
    strategies = {"default": DefaultStrategy, "aggressive": AggressiveStrategy}
    return strategies.get(name, DefaultStrategy)()
