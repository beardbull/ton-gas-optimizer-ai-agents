# server.py - MCP Endpoint for AI Agents (FastAPI)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.agents import AgentNetwork
from core.strategies import get_strategy

app = FastAPI(title="TON Gas Optimizer MCP")

class OptimizationRequest(BaseModel):
    ops: int
    gas_nano: int
    load_percent: int
    balance_ton: float = 1.0
    strategy_name: str = "default"

@app.post("/mcp/tools/optimize_gas")
async def optimize_gas(req: OptimizationRequest):
    try:
        strategy = get_strategy(req.strategy_name)
        network = AgentNetwork()
        pipeline_result = network.run_pipeline(req.ops, req.gas_nano, req.load_percent, req.balance_ton)
        result = pipeline_result["recommendation"]
        result["batch"] = strategy.should_batch(req.ops, req.load_percent, req.gas_nano)
        result["savings_percent"] = strategy.estimate_savings(req.ops, req.gas_nano, req.load_percent)
        result["reason"] = strategy.get_reason(req.ops, req.load_percent, req.gas_nano)
        return {"status": "success", "recommendation": result, "metadata": pipeline_result["agents_status"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "TON Gas Optimizer MCP"}
