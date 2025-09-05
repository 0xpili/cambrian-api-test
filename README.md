# Cambrian API Test Suite

Complete testing setup for the **Cambrian API**. This repository contains Python clients, workflow demos, and Postman collections for testing all major API endpoints.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- `requests` library: `pip install requests`
- (Optional) Postman for GUI testing

### Your API Key
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
nano .env
```

```
# .env file contents
CAMBRIAN_API_KEY=your_api_key_here
CAMBRIAN_BASE_URL=https://opabinia.cambrian.network/api/v1
```

### Run the Demo
```bash
# Basic connectivity test
python3 cambrian_client.py

# Comprehensive workflow demo
python3 demo_workflows.py
```

## 📁 Files Overview

| File | Description |
|------|-------------|
| `cambrian_client.py` | Complete Python API client with all endpoints |
| `demo_workflows.py` | Demonstrates key workflows with real data |
| `Cambrian_API.postman_collection.json` | Postman collection for GUI testing |
| `README.md` | This documentation file |

## 🔥 Key Features Tested

### ✅ **Token Discovery & Research**
- Find trending tokens by volume/price change
- Get comprehensive token details and metadata
- Real-time price data and historical trends
- Market intelligence dashboard

### ✅ **Price Data & Analytics** 
- Current prices (single and multi-token)
- Historical price data (hourly)
- OHLCV candlestick data for charting
- Price change percentages and volume

### ✅ **Portfolio Management**
- Wallet token balance tracking
- Balance history over time
- Multi-token portfolio analysis

### ✅ **Trading Analytics**
- Buy/sell volume breakdown
- Trading statistics and ratios
- Recent transaction history
- Top traders leaderboard

### ✅ **Liquidity Pool Analysis**
- Find pools containing specific tokens
- Pool performance metrics and fees
- TVL (Total Value Locked) data
- Pool transaction history

## 📊 Sample Output

### Trending Tokens by Volume
```
Found 10 trending tokens by 24h volume:
  1. SOL      | $203.5987 |  -2.67% 📉 | Vol: $3,714,048,756
  2. JLP      | $  5.4199 |  -1.28% 📉 | Vol: $72,478,922
  3. CARDS    | $  0.1778 | -12.10% 📉 | Vol: $56,137,468
  4. cbBTC    | $110839.68|  -1.06% 📉 | Vol: $46,898,543
  5. JitoSOL  | $249.8843 |  -2.69% 📉 | Vol: $25,205,276
```

### Token Details (SOL Example)
```
SOL Details:
  symbol: SOL
  name: Wrapped SOL
  decimals: 9
  priceUSD: 203.59872727937682
  volume24hUSD: 3728953853.681366
  holderCount: 3168797
  totalSupply: 16947231.32550178
  fdvUSD: 3450434728.7813487
```

## 🛠️ API Client Features

### Response Format Handling
The Cambrian API returns data in a database-style format:
```json
[{
  "columns": [{"name": "tokenAddress", "type": "String"}, ...],
  "data": [["So111...", "SOL", 203.59], ...],
  "rows": 1
}]
```

Our client includes a `parse_response()` method that converts this to user-friendly dictionaries:
```python
# Raw API response -> User-friendly format
raw_data = cambrian.get_trending_tokens()
parsed_data = cambrian.parse_response(raw_data)
# Now you can access: parsed_data[0]['symbol'], parsed_data[0]['priceUSD'], etc.
```

### Error Handling
- Automatic retry logic
- Clear error messages for common issues (401, 429, etc.)
- Connection timeout management
- JSON parsing error handling

## 📮 Postman Setup

1. **Import Collection**: Import `Cambrian_API.postman_collection.json`
2. **Environment Variables**: The collection includes these pre-configured variables:
   - `base_url`: https://opabinia.cambrian.network/api/v1
   - `api_key`: Your API key (your_api_key_here)
   - `sol_address`: SOL token address for testing

3. **Authentication**: All requests automatically include the `X-API-KEY` header

## 🔧 Common Use Cases

### 1. **Market Intelligence Dashboard**
```python
# Get trending tokens
trending = cambrian.get_trending_tokens(limit=10)
tokens = cambrian.parse_response(trending)

# Get current prices
addresses = [token['tokenAddress'] for token in tokens[:5]]
prices = cambrian.get_multiple_prices(addresses)
price_data = cambrian.parse_response(prices)

# Combine data for dashboard
for token, price in zip(tokens, price_data):
    print(f"{token['symbol']}: ${price['priceUSD']:.4f}")
```

### 2. **Portfolio Tracking**
```python
# Track wallet balances
wallet = "YOUR_WALLET_ADDRESS"
balances = cambrian.get_holder_balances(wallet)
portfolio = cambrian.parse_response(balances)

total_usd = sum(token['balanceUSD'] for token in portfolio)
print(f"Total Portfolio Value: ${total_usd:,.2f}")
```

### 3. **Token Research Pipeline**
```python
# 1. Find trending token
trending = cambrian.parse_response(cambrian.get_trending_tokens(limit=1))
token_address = trending[0]['tokenAddress']

# 2. Get detailed metrics
details = cambrian.parse_response(cambrian.get_token_details(token_address))
trades = cambrian.parse_response(cambrian.get_trade_statistics([token_address]))

# 3. Analyze pools
pools = cambrian.parse_response(cambrian.search_token_pools(token_address))

print(f"Token: {details[0]['symbol']}")
print(f"Market Cap: ${details[0]['fdvUSD']:,.2f}")
print(f"24h Volume: ${trades[0]['volume24hUSD']:,.2f}")
print(f"Available Pools: {len(pools)}")
```

## 🌐 Available Endpoints

### Token Discovery
- `GET /solana/trending-tokens` - Hot tokens by metrics
- `GET /solana/tokens` - All available tokens
- `GET /solana/token-details` - Comprehensive token info

### Price Data
- `GET /solana/price-current` - Current price
- `GET /solana/price-multi` - Multiple prices
- `GET /solana/price-hour` - Historical hourly prices
- `GET /solana/ohlcv/token` - Candlestick data

### Portfolio Management
- `GET /solana/holder-token-balances` - Wallet holdings
- `GET /solana/wallet-balance-history` - Balance over time

### Trading Analytics
- `GET /solana/trade-statistics` - Buy/sell breakdown
- `GET /solana/token-transactions` - Recent transactions
- `GET /solana/traders/leaderboard` - Top traders

### Pool Analysis
- `GET /solana/token-pool-search` - Find pools
- `GET /solana/orca/pool` - Pool details
- `GET /solana/orca/pools/fee-metrics` - Performance metrics
- `GET /solana/pool-transactions` - Pool activity

## 📈 Next Steps

### Potential Enhancements
1. **Historical Analysis**: Add time-series analysis tools
2. **Alert System**: Price/volume change notifications
3. **Portfolio Optimization**: Risk/return calculations
4. **Arbitrage Detection**: Cross-DEX price comparisons
5. **Automated Trading**: Signal generation and execution

### Integration Ideas
1. **Discord Bot**: Real-time market updates
2. **Web Dashboard**: Interactive portfolio tracking
3. **Mobile App**: Push notifications for price alerts
4. **Excel Plugin**: Import live market data
5. **Trading Bot**: Automated DeFi strategies

## 📚 Documentation & Support

- **Full API Docs**: https://docs.cambrian.org
- **OpenAPI Spec**: https://opabinia.cambrian.network/openapi.json
- **Discord Support**: https://discord.com/channels/1375182661202481172/1376641098516271155

## 🔐 Security Notes

- Use environment variables for API keys: `os.environ['CAMBRIAN_API_KEY']`
- Copy `.env.example` to `.env` and add your API key
- Rate limits apply - monitor 429 responses
- Keep API keys secure and never commit to public repositories

---

**Happy testing! 🚀** The Cambrian API provides comprehensive Solana DeFi analytics for building sophisticated trading tools, portfolio managers, and market intelligence systems.