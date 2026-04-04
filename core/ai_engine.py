# core/ai_engine.py - AI Recommendation Engine via OpenRouter
import os
import json

def get_api_key():
    """Get API key: Streamlit Secrets (cloud) or .env (local)"""
    try:
        import streamlit as st
        if st.secrets.get("openrouter", {}).get("api_key"):
            return st.secrets["openrouter"]["api_key"]
    except:
        pass
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        key = os.getenv("OPENROUTER_API_KEY")
        if key and key.startswith("sk-or-"):
            return key
    except:
        pass
    
    return None

def get_ai_recommendation(ops: int, load: int, gas: int, balance: float = 0) -> dict:
    """Get AI-powered batching recommendation via OpenRouter"""
    api_key = get_api_key()
    
    # Если ключа нет — сразу фолбэк
    if not api_key:
        return get_rule_based_recommendation(ops, load, gas, balance)
    
    try:
        from openai import OpenAI
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        
        prompt = f"""
Analyze TON network: {load}% load, {gas} nanoTON gas, {ops} ops.
Should agent batch transactions? Reply ONLY JSON:
{{"batch": bool, "reason": "string", "estimated_savings_percent": number, "confidence": number, "alternative_action": "string"}}
"""
        resp = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300,
            timeout=30
        )
        
        content = resp.choices[0].message.content.strip()
        if "```json" in content: content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content: content = content.split("```")[1].split("```")[0].strip()
        
        result = json.loads(content)
        return {
            "batch": result.get("batch", False),
            "reason": result.get("reason", ""),
            "savings_percent": result.get("estimated_savings_percent", 0),
            "confidence": result.get("confidence", 85),
            "alternative_action": result.get("alternative_action", ""),
            "source": "AI (OpenRouter)"
        }
    except Exception as e:
        return get_rule_based_recommendation(ops, load, gas, balance)

def get_rule_based_recommendation(ops: int, load: int, gas: int, balance: float) -> dict:
    """Fallback: rule-based logic (no API required)"""
    if ops >= 5 and load < 50:
        return {"batch": True, "reason": "High ops + low load", "savings_percent": 45, "confidence": 85, "alternative_action": "", "source": "Rule-based"}
    elif load > 80:
        return {"batch": False, "reason": "Network congestion", "savings_percent": 0, "confidence": 90, "alternative_action": "Wait 5-10 min", "source": "Rule-based"}
    elif ops < 3:
        return {"batch": False, "reason": "Too few operations", "savings_percent": 0, "confidence": 80, "alternative_action": "Execute separately", "source": "Rule-based"}
    elif gas > 7000:
        return {"batch": True, "reason": "High gas price", "savings_percent": 35, "confidence": 75, "alternative_action": "", "source": "Rule-based"}
    else:
        sb = ops >= 3
        return {"batch": sb, "reason": "Standard conditions", "savings_percent": 25 if sb else 0, "confidence": 80, "alternative_action": "" if sb else "Wait for lower load", "source": "Rule-based"}
