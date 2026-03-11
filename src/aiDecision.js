// src/aiDecision.js
// AI decision logic using Gemini API for Lablab.ai hackathon

const { GoogleGenerativeAI } = require('@google/generative-ai');

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

/**
 * AI decides whether to batch transactions based on network conditions
 * @param {Array} operations - List of pending operations
 * @param {number} networkLoad - Current network load (0-100)
 * @param {number} gasPrice - Current gas price in nanoTON
 * @returns {Promise<Object>} Decision with reason and estimated savings
 */
async function shouldBatch(operations, networkLoad, gasPrice) {
  // Fallback if no API key (for local testing without Gemini)
  if (!process.env.GEMINI_API_KEY) {
    return {
      shouldBatch: operations.length >= 3 && networkLoad < 80,
      reason: 'Fallback heuristic: batch if 3+ ops and load < 80%',
      estimatedSavings: '71.5%',
      confidence: 0.85
    };
  }

  try {
    const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
    
    const prompt = `
You are a TON blockchain gas optimization AI agent.

Current state:
- Operations pending: ${operations.length}
- Network load: ${networkLoad}%
- Gas price: ${gasPrice} nanoTON

Should these operations be batched into one transaction?
Consider: gas savings, slippage risk, network congestion, MEV protection.

Respond with valid JSON only:
{
  "shouldBatch": boolean,
  "reason": "string explaining decision",
  "estimatedSavings": "string like '71.5%'",
  "confidence": number between 0 and 1
}
`;

    const result = await model.generateContent(prompt);
    const response = result.response.text();
    
    // Extract JSON from response (Gemini may add text around it)
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[0]);
    }
    
    // Fallback if parsing fails
    return {
      shouldBatch: operations.length >= 3,
      reason: 'AI parsing fallback',
      estimatedSavings: '~70%',
      confidence: 0.7
    };
    
  } catch (error) {
    console.error('Gemini API error:', error.message);
    return {
      shouldBatch: operations.length >= 3 && networkLoad < 80,
      reason: 'Fallback: API error',
      estimatedSavings: '~70%',
      confidence: 0.6
    };
  }
}

module.exports = { shouldBatch };
