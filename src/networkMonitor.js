// src/NetworkMonitor.js
// TON Network load monitor (Testnet/Mainnet)

const { TonClient } = require('@ton/ton');

class NetworkMonitor {
  constructor(network = 'testnet') {
    this.endpoint = network === 'mainnet' 
      ? 'https://toncenter.com/api/v2/jsonRPC'
      : 'https://testnet.toncenter.com/api/v2/jsonRPC';
    
    this.client = new TonClient({ endpoint: this.endpoint });
  }

  // Get current network load (0.0 - 1.0)
  // Fallback: timestamp-based pseudo-random if API fails
  async getNetworkLoad() {
    try {
      // Fetch latest masterchain info
      const master = await this.client.getMasterchainInfo();
      
      // API v2 format: last?.seqno or seqno
      const seqno = master.last?.seqno || master.seqno || 0;
      
      // If seqno=0, API returned invalid data → use fallback
      if (seqno === 0) {
        return this._fallbackLoad('API returned seqno = 0 (invalid data)');
      }
      
      // Generate pseudo-load 0.3-0.9 based on block number (for demo)
      const pseudoLoad = 0.3 + ((seqno % 100) / 100) * 0.6;
      
      return {
        seqno,
        load: parseFloat(pseudoLoad.toFixed(2)),
        note: 'Load estimated from block seqno (demo mode)'
      };
      
    } catch (error) {
      console.warn('⚠️ Network API failed, using fallback:', error.message);
      return this._fallbackLoad(error.message);
    }
  }

  // Fallback: dynamic load based on timestamp (changes every ~10 sec)
  _fallbackLoad(reason) {
    const now = Date.now();
    // Pseudo-random but deterministic per 10-second window
    const pseudoLoad = 0.3 + ((now % 10000) / 10000) * 0.6;
    
    return {
      seqno: null,
      load: parseFloat(pseudoLoad.toFixed(2)),
      note: `Fallback: timestamp-based load (API unavailable) — CHANGES EVERY 10 SEC!`
    };
  }
}

module.exports = { NetworkMonitor };