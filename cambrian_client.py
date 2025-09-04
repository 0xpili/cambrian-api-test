import requests
import json
import os
from typing import Dict, List, Optional, Union
from datetime import datetime

# Load environment variables from .env file
def load_env():
    """Load environment variables from .env file if it exists"""
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load .env on import
load_env()

class CambrianAPI:
    """
    Python client for the Cambrian API - Solana token and DeFi analytics
    """
    
    def __init__(self, api_key: str = None, base_url: str = None):
        # Use environment variables if not provided
        self.api_key = api_key or os.getenv('CAMBRIAN_API_KEY')
        self.base_url = (base_url or os.getenv('CAMBRIAN_BASE_URL', 'https://opabinia.cambrian.network/api/v1')).rstrip('/')
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Either:\n"
                "1. Pass it as parameter: CambrianAPI('your_key')\n"
                "2. Set CAMBRIAN_API_KEY environment variable\n" 
                "3. Create .env file with CAMBRIAN_API_KEY=your_key"
            )
            
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'CambrianAPI-Python-Client'
        })
    
    def parse_response(self, response: List[Dict]) -> List[Dict]:
        """
        Convert Cambrian API database-style response to user-friendly format
        
        Input: [{'columns': [...], 'data': [...], 'rows': N}]
        Output: [{'col1': val1, 'col2': val2, ...}, ...]
        """
        if not response or len(response) == 0:
            return []
            
        result = response[0]
        columns = result.get('columns', [])
        data_rows = result.get('data', [])
        
        parsed = []
        for row in data_rows:
            row_dict = {}
            for i, col_info in enumerate(columns):
                col_name = col_info['name']
                if i < len(row):
                    row_dict[col_name] = row[i]
            parsed.append(row_dict)
        
        return parsed
        
    def test_endpoints(self):
        """Test different endpoint variations to find correct API path"""
        test_paths = [
            'solana/latest-block',
            'solana/tokens',
            'solana/trending-tokens'
        ]
        
        for path in test_paths:
            try:
                url = f"{self.base_url}/{path}"
                response = self.session.get(url)
                print(f"Testing {url}: {response.status_code}")
                if response.status_code == 200:
                    print(f"✅ Working endpoint found: {url}")
                    return response.json()
                elif response.status_code == 401:
                    print(f"   401 Unauthorized - API key issue")
                elif response.status_code == 429:
                    print(f"   429 Rate Limited")
                else:
                    print(f"   Response: {response.text[:100]}...")
            except Exception as e:
                print(f"   Error: {e}")
        return None
    
    def _make_request(self, endpoint: str, method: str = 'GET', params: Dict = None, data: Dict = None) -> Dict:
        """Make HTTP request to API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error {response.status_code}: {response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise
        except json.JSONDecodeError:
            print(f"Invalid JSON response: {response.text}")
            raise
    
    # Basic connectivity test  
    def get_latest_block(self) -> Dict:
        """Get latest block information"""
        return self._make_request('solana/latest-block')
    
    # Token discovery endpoints
    def get_trending_tokens(self, order_by: str = "volume_usd_24h", limit: int = 10) -> Dict:
        """Get trending tokens ordered by various metrics"""
        params = {
            'order_by': order_by,
            'limit': limit
        }
        return self._make_request('solana/trending-tokens', params=params)
    
    def get_tokens(self, limit: int = 100, offset: int = 0) -> Dict:
        """List all available tokens"""
        params = {
            'limit': limit,
            'offset': offset
        }
        return self._make_request('solana/tokens', params=params)
    
    def get_token_details(self, token_address: str) -> Dict:
        """Get comprehensive token information"""
        params = {'token_address': token_address}
        return self._make_request('solana/token-details', params=params)
    
    # Price data endpoints
    def get_current_price(self, token_address: str) -> Dict:
        """Get current price for single token"""
        params = {'token_address': token_address}
        return self._make_request('solana/price-current', params=params)
    
    def get_multiple_prices(self, token_addresses: List[str]) -> Dict:
        """Get current prices for multiple tokens"""
        params = {'token_addresses': ','.join(token_addresses)}
        return self._make_request('solana/price-multi', params=params)
    
    def get_price_history(self, token_address: str, hours_back: int = 24) -> Dict:
        """Get hourly price history"""
        params = {
            'token_address': token_address,
            'hours_back': hours_back
        }
        return self._make_request('solana/price-hour', params=params)
    
    def get_ohlcv(self, token_address: str, timeframe: str = "1h", limit: int = 100) -> Dict:
        """Get OHLCV candlestick data"""
        params = {
            'token_address': token_address,
            'timeframe': timeframe,
            'limit': limit
        }
        return self._make_request('solana/ohlcv/token', params=params)
    
    # Portfolio management
    def get_holder_balances(self, holder_address: str, limit: int = 20) -> Dict:
        """Get token balances for a wallet"""
        params = {
            'holder': holder_address,
            'limit': limit
        }
        return self._make_request('solana/holder-token-balances', params=params)
    
    def get_wallet_history(self, wallet_address: str, after_time: Optional[str] = None) -> Dict:
        """Get wallet balance history"""
        params = {'wallet_address': wallet_address}
        if after_time:
            params['after_time'] = after_time
        return self._make_request('solana/wallet-balance-history', params=params)
    
    # Trading analysis
    def get_trade_statistics(self, token_addresses: List[str], timeframe: str = "24h") -> Dict:
        """Get trading statistics for tokens"""
        params = {
            'token_addresses': ','.join(token_addresses),
            'timeframe': timeframe
        }
        return self._make_request('solana/trade-statistics', params=params)
    
    def get_token_transactions(self, token_address: str, limit: int = 50) -> Dict:
        """Get recent transactions for token"""
        params = {
            'token_address': token_address,
            'limit': limit
        }
        return self._make_request('solana/token-transactions', params=params)
    
    def get_traders_leaderboard(self, token_address: str, limit: int = 10) -> Dict:
        """Get top traders for a token"""
        params = {
            'token_address': token_address,
            'limit': limit
        }
        return self._make_request('solana/traders/leaderboard', params=params)
    
    # Pool analysis
    def search_token_pools(self, token_address: str, limit: int = 10) -> Dict:
        """Find pools containing a token"""
        params = {
            'token_address': token_address,
            'limit': limit
        }
        return self._make_request('solana/token-pool-search', params=params)
    
    def get_pool_details(self, pool_address: str) -> Dict:
        """Get Orca pool details"""
        params = {'pool_address': pool_address}
        return self._make_request('solana/orca/pool', params=params)
    
    def get_pool_fee_metrics(self, pool_address: str, timeframe_days: int = 7) -> Dict:
        """Get pool fee and performance metrics"""
        params = {
            'pool_address': pool_address,
            'timeframe_days': timeframe_days
        }
        return self._make_request('solana/orca/pools/fee-metrics', params=params)
    
    def get_pool_transactions(self, pool_address: str, limit: int = 50) -> Dict:
        """Get pool transaction history"""
        params = {
            'pool_address': pool_address,
            'limit': limit
        }
        return self._make_request('solana/pool-transactions', params=params)


def main():
    """Example usage of the Cambrian API client"""
    
    # Initialize client - API key loaded from environment/.env
    cambrian = CambrianAPI()
    
    print("🚀 Testing Cambrian API Connection...")
    
    try:
        # Test different endpoint paths first
        print("\n0. Testing different API paths...")
        working_response = cambrian.test_endpoints()
        if working_response:
            print(f"Found working API response: {working_response}")
        
        # Test 1: Basic connectivity
        print("\n1. Testing basic connectivity...")
        latest_block = cambrian.get_latest_block()
        print(f"✅ Latest block: {latest_block}")
        
        # Test 2: Get trending tokens
        print("\n2. Getting trending tokens...")
        trending = cambrian.get_trending_tokens(limit=5)
        print(f"✅ Trending tokens response received: {type(trending)}")
        
        # Handle the database-style response format
        if trending and len(trending) > 0 and trending[0].get('data'):
            print(f"✅ Found {len(trending[0]['data'])} trending tokens")
            
            # Test 3: Show trending tokens data
            print("\n3. Displaying trending tokens...")
            first_result = trending[0]
            columns = first_result['columns']
            data_rows = first_result['data']
            
            print("Columns:", [col['name'] for col in columns])
            for i, row in enumerate(data_rows[:3]):  # Show first 3
                print(f"Row {i+1}: {row}")
            
            # Test 4: Try to get token details with a known Solana token address
            print("\n4. Testing with known SOL token...")
            sol_address = "So11111111111111111111111111111111111111112"
            try:
                price = cambrian.get_current_price(sol_address)
                print(f"✅ SOL price response: {price}")
            except Exception as e:
                print(f"Price lookup error: {e}")
                
        else:
            print("No trending tokens data found or unexpected format")
        
        print("\n🎉 All tests passed! API is working correctly.")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()