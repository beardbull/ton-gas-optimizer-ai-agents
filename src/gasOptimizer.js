// src/GasOptimizer.js
// TON Gas Optimizer - Core logic for AI agents

class GasOptimizer {
  constructor() {
    this.baseGasCost = 0.0050; // base cost per op in TON
    this.batchOverhead = 0.0012; // batching overhead
  }

  // Analyze operations and calculate gas savings
  // Returns: { normalCost, optimizedCost, saved, savingsPercent, networkLoad }
  analyze(operations, options = {}) {
    const { networkLoad = 0.5 } = options;
    const count = operations.length;
    
    // Base savings: 50% for 1 op, scales to 75% for 50+ ops
    const baseSavings = 0.50 + (Math.min(count, 50) / 50) * 0.25;
    
    // Bonus from network load: up to +25%
    const loadBonus = networkLoad * 0.25;
    
    // Cap at 95% to prevent negative costs in edge cases
    const savingsPercent = Math.min(95, (baseSavings + loadBonus) * 100);
    
    const normalCost = count * this.baseGasCost;
    const optimizedCost = normalCost * (1 - savingsPercent / 100);
    
    return {
      operations: count,
      normalCost: `${normalCost.toFixed(4)} TON`,
      optimizedCost: `${optimizedCost.toFixed(4)} TON`,
      saved: `${(normalCost - optimizedCost).toFixed(4)} TON`,
      savingsPercent: `${savingsPercent.toFixed(1)}%`,
      networkLoad: `${(networkLoad * 100).toFixed(0)}%`
    };
  }

  // Recommend batching for 5+ operations
  shouldBatch(operations) {
    return operations.length >= 5;
  }

  // Full batch estimate with recommendation
  estimateBatch(operations, options = {}) {
    const analysis = this.analyze(operations, options);
    
    return {
      shouldBatch: this.shouldBatch(operations),
      ...analysis,
      recommendation: this.shouldBatch(operations) 
        ? 'Batching recommended - significant savings' 
        : 'Batching not recommended - too few operations'
    };
  }
}

module.exports = { GasOptimizer };