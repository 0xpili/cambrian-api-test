# Cambrian API Test Suite

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![API Docs](https://img.shields.io/badge/docs-cambrian.org-green.svg)](https://docs.cambrian.org)

Complete testing framework for the **Cambrian API** - A comprehensive Solana DeFi analytics platform. This repository provides Python clients, workflow demonstrations, and Postman collections for all major API endpoints.


## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/0xpili/cambrian-api-test.git
cd cambrian-api-test
pip install requests
```

### 2. Configure API Key
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
nano .env
```

```bash
# .env file contents
CAMBRIAN_API_KEY=your_api_key_here
CAMBRIAN_BASE_URL=https://opabinia.cambrian.network/api/v1
```

### 3. Run the Demo
```bash
# Basic connectivity test
python3 cambrian_client.py

# Comprehensive workflow demo
python3 demo_workflows.py
```

## 📁 Repository Structure

```
cambrian-api-test/
├── cambrian_client.py              # Complete Python API client
├── demo_workflows.py               # Workflow demonstrations
├── Cambrian_API.postman_collection.json  # Postman collection
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🔑 Getting Your API Key

1. **Sign up** at [Cambrian Platform](https://cambrian.org)
2. **Generate API Key** from your dashboard
3. **Add to `.env`** file as shown above
4. **Test connection** with `python3 cambrian_client.py`

## 💻 Python Client Usage

### Basic Usage
```python
from cambrian_client import CambrianAPI

# Initialize (reads from .env automatically)
cambrian = CambrianAPI()

# Or pass API key directly
cambrian = CambrianAPI(api_key="your_key_here")
```

### Token Discovery
```python
# Get trending tokens by volume
trending = cambrian.get_trending_tokens(order_by="volume_usd_24h", limit=10)
tokens = cambrian.parse_response(trending)

for token in tokens:
    print(f"{token['symbol']}: ${token['currentPriceUSD']:.4f}")
```

### Portfolio Tracking
```python
# Monitor wallet balances
wallet = "your_wallet_address"
balances = cambrian.get_holder_balances(wallet)
portfolio = cambrian.parse_response(balances)

total_value = sum(token['balanceUSD'] for token in portfolio)
print(f"Total Portfolio: ${total_value:,.2f}")
```

### Price Analysis
```python
# Get multiple token prices
token_addresses = ["So111...", "27G8Mt..."]  # SOL, JLP
prices = cambrian.get_multiple_prices(token_addresses)
price_data = cambrian.parse_response(prices)

for price in price_data:
    print(f"{price['symbol']}: ${price['priceUSD']:.6f}")
```

## 📮 Postman Setup

### Import Collection
1. **Open Postman** and click "Import"
2. **Select** `Cambrian_API.postman_collection.json`
3. **Update Environment** variables:
   - `api_key`: Your actual API key
   - `base_url`: https://opabinia.cambrian.network/api/v1

### Pre-configured Requests
- **🏁 Basic Connectivity** - Health checks and latest block
- **🔥 Token Discovery** - Trending tokens and search
- **💰 Price Data** - Current prices and historical data
- **👛 Portfolio Management** - Wallet tracking
- **📊 Trading Analytics** - Volume and transaction analysis  
- **🏊 Pool Analysis** - Liquidity pool metrics

## 🛠️ Common Workflows

### 1. Market Intelligence Dashboard
```python
def create_market_dashboard():
    cambrian = CambrianAPI()
    
    # Top volume tokens
    trending = cambrian.parse_response(
        cambrian.get_trending_tokens(order_by="volume_usd_24h", limit=5)
    )
    
    # Latest market data
    latest_block = cambrian.parse_response(cambrian.get_latest_block())[0]
    
    return {
        'trending_tokens': trending,
        'latest_block': latest_block['blockNumber'],
        'timestamp': latest_block['blockTime']
    }
```

### 2. Token Research Pipeline
```python
def analyze_token(token_address):
    cambrian = CambrianAPI()
    
    # Get comprehensive data
    details = cambrian.parse_response(cambrian.get_token_details(token_address))[0]
    price = cambrian.parse_response(cambrian.get_current_price(token_address))[0]
    pools = cambrian.parse_response(cambrian.search_token_pools(token_address))
    
    return {
        'symbol': details['symbol'],
        'price': price['priceUSD'],
        'market_cap': details['fdvUSD'],
        'volume_24h': details['volume24hUSD'],
        'available_pools': len(pools)
    }
```

### 3. Portfolio Monitoring
```python
def track_portfolio(wallet_address):
    cambrian = CambrianAPI()
    
    # Current holdings
    balances = cambrian.parse_response(
        cambrian.get_holder_balances(wallet_address)
    )
    
    # Historical performance
    history = cambrian.parse_response(
        cambrian.get_wallet_history(wallet_address)
    )
    
    total_usd = sum(token['balanceUSD'] for token in balances)
    top_holdings = sorted(balances, key=lambda x: x['balanceUSD'], reverse=True)[:5]
    
    return {
        'total_value_usd': total_usd,
        'token_count': len(balances),
        'top_holdings': top_holdings,
        'history_points': len(history)
    }
```

## 📊 Response Format

The Cambrian API returns data in a database-style format:

```json
[{
  "columns": [
    {"name": "tokenAddress", "type": "String"},
    {"name": "symbol", "type": "String"},
    {"name": "priceUSD", "type": "Float64"}
  ],
  "data": [
    ["So111...", "SOL", 203.45],
    ["27G8M...", "JLP", 5.42]
  ],
  "rows": 2
}]
```

Our client automatically converts this to user-friendly dictionaries:

```python
# Use parse_response() to convert
raw_data = cambrian.get_trending_tokens()
friendly_data = cambrian.parse_response(raw_data)

# Now access as: friendly_data[0]['symbol'], friendly_data[0]['priceUSD']
```

## 🔧 Available Endpoints

### Token Discovery
- `GET /solana/trending-tokens` - Hot tokens by various metrics
- `GET /solana/tokens` - All available tokens with pagination
- `GET /solana/token-details` - Comprehensive token metadata

### Price Data
- `GET /solana/price-current` - Real-time single token price
- `GET /solana/price-multi` - Batch price lookup
- `GET /solana/price-hour` - Historical hourly prices
- `GET /solana/ohlcv/token` - Candlestick/OHLCV data

### Portfolio Management
- `GET /solana/holder-token-balances` - Wallet token holdings
- `GET /solana/wallet-balance-history` - Balance changes over time

### Trading Analytics
- `GET /solana/trade-statistics` - Buy/sell volume breakdown
- `GET /solana/token-transactions` - Recent transaction history
- `GET /solana/traders/leaderboard` - Top traders for tokens

### Pool Analysis
- `GET /solana/token-pool-search` - Find pools containing tokens
- `GET /solana/orca/pool` - Detailed pool information
- `GET /solana/orca/pools/fee-metrics` - Pool performance and APR
- `GET /solana/pool-transactions` - Pool transaction history

## 🚨 Security Best Practices

### ✅ Do's
- ✅ Store API keys in `.env` files (excluded from git)
- ✅ Use environment variables in production
- ✅ Implement proper error handling and rate limiting
- ✅ Monitor API usage and costs

### ❌ Don'ts
- ❌ Never commit API keys to version control
- ❌ Don't hardcode credentials in source code
- ❌ Avoid exposing keys in logs or error messages
- ❌ Don't share environment files publicly

### Production Environment
```python
import os

# Production setup
api_key = os.environ.get('CAMBRIAN_API_KEY')
if not api_key:
    raise ValueError("CAMBRIAN_API_KEY environment variable required")

cambrian = CambrianAPI(api_key=api_key)
```

## 📈 Sample Output

```
🌟 Cambrian API - Common Workflows Demo
This demo showcases the key use cases for Solana DeFi analytics

============================================================
🚀 WORKFLOW 1: Token Research & Analysis
============================================================

📊 Step 1: Discover Trending Tokens
----------------------------------------
Found 10 trending tokens by 24h volume (showing top 10):
   1. SOL      | $204.4018 |  -2.83% 📉 | Vol: $3,767,189,918
   2. JLP      | $  5.4279 |  -1.33% 📉 | Vol: $73,385,981
   3. CARDS    | $  0.1822 | -11.24% 📉 | Vol: $53,644,481
   4. cbBTC    | $111631.77|  -0.22% 📉 | Vol: $48,254,402
   5. JitoSOL  | $251.0687 |  -2.78% 📉 | Vol: $26,240,658
   6. WBTC     | $111699.12|  -0.20% 📉 | Vol: $20,411,519
   7. TRUMP    | $  8.3087 |  -1.40% 📉 | Vol: $19,119,823
   8. PASTERNAK| $  0.0720 | +20.99% 📈 | Vol: $18,131,542
   9. AnswerBook| $  0.0011 | -80.66% 📉 | Vol: $14,838,213
  10. WLFI     | $  0.1889 | -13.13% 📉 | Vol: $13,603,422

============================================================
🚀 WORKFLOW 3: Multi-Token Price Analysis
============================================================

📊 Real-time Price Comparison (Top 5 Trending Tokens):
================================================================================
Token        Current Price   24h Volume      24h Change      Trend
--------------------------------------------------------------------------------
SOL          $204.7589       $3.8B           -2.66%          📉 DOWN
JLP          $5.4312         $73.5M          -1.27%          📉 DOWN
CARDS        $0.183578       $53.7M          -10.56%         📉 DOWN
cbBTC        $111,752.02     $48.3M          -0.11%          📉 DOWN
JitoSOL      $251.1503       $26.2M          -2.75%          📉 DOWN
================================================================================

============================================================
🚀 WORKFLOW 4: Trading Analytics Deep Dive
============================================================

📋 Trading Analysis Summary (24h Period)
====================================================================================================
Token    Total Trades Buy/Sell Ratio  Volume Ratio    Sentiment    Total Volume
----------------------------------------------------------------------------------------------------
SOL      11.0M        28.2%/71.8%     21.4%/78.6%     🔴 BEARISH    $3.8B
JLP      122.0K       45.7%/54.3%     49.7%/50.3%     🟡 NEUTRAL    $73.4M
CARDS    51.5K        50.9%/49.1%     48.5%/51.5%     🟡 NEUTRAL    $49.8M
cbBTC    81.5K        53.4%/46.6%     51.4%/48.6%     🟡 NEUTRAL    $48.9M
JitoSOL  57.1K        50.0%/50.0%     54.9%/45.1%     🟡 NEUTRAL    $26.1M
====================================================================================================
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add feature"`
5. Push to your fork: `git push origin feature-name`
6. Create a Pull Request

## 📚 Resources

- **API Documentation**: https://docs.cambrian.org
- **OpenAPI Specification**: https://opabinia.cambrian.network/openapi.json
- **Discord Community**: https://discord.gg/cambrian-api
- **GitHub Issues**: Report bugs and request features

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🔗 Related Projects

- [Cambrian Platform](https://cambrian.org) - Main platform
- [Solana Documentation](https://docs.solana.com) - Solana blockchain docs
- [Orca Protocol](https://www.orca.so) - Solana DEX integration

---

**Happy Building!** 🚀 Use this test suite to explore Solana DeFi analytics and build sophisticated trading tools, portfolio managers, and market intelligence systems.