// demo/server.js - Simple HTTP server for Lablab.ai demo
const http = require('http');

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.method === 'GET' && req.url === '/health') {
    res.statusCode = 200;
    res.end(JSON.stringify({ 
      status: 'ok', 
      timestamp: new Date().toISOString(),
      project: 'TON Gas Optimizer AI'
    }));
    return;
  }
  
  if (req.method === 'POST' && req.url === '/api/optimize') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', async () => {
      try {
        const { operations = [], networkLoad = 50, gasPrice = 5000 } = JSON.parse(body);
        
        // AI decision logic (fallback mode)
        const shouldBatch = operations.length >= 3 && networkLoad < 80;
        
        // Simple optimization calculation
        const baseCost = operations.length * 0.005;
        const optimizedCost = shouldBatch ? baseCost * 0.285 : baseCost;
        const savings = ((baseCost - optimizedCost) / baseCost * 100).toFixed(1);
        
        res.statusCode = 200;
        res.end(JSON.stringify({
          aiDecision: {
            shouldBatch,
            reason: shouldBatch 
              ? `Batching recommended: ${operations.length} ops at ${networkLoad}% load`
              : `No batching: ${operations.length < 3 ? 'too few ops' : 'high network load'}`,
            estimatedSavings: `${savings}%`,
            confidence: 0.85
          },
          optimization: {
            normalCost: `${baseCost.toFixed(4)} TON`,
            optimizedCost: `${optimizedCost.toFixed(4)} TON`,
            savings: `${savings}%`
          },
          timestamp: new Date().toISOString()
        }));
      } catch (error) {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: error.message }));
      }
    });
    return;
  }
  
  res.statusCode = 404;
  res.end(JSON.stringify({ error: 'Not found' }));
});

server.listen(PORT, () => {
  console.log(`🚀 TON Gas Optimizer AI running on port ${PORT}`);
  console.log(`📡 Health: http://localhost:${PORT}/health`);
  console.log(`🔧 API: POST http://localhost:${PORT}/api/optimize`);
});
