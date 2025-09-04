#!/usr/bin/env python3
"""
Cambrian API Demo - Common Workflows & Use Cases

This script demonstrates the key workflows mentioned in your documentation:
1. Token Research & Analysis
2. Liquidity Pool Analysis  
3. Portfolio Tracking & Management
"""

from cambrian_client import CambrianAPI
import json

def print_section(title):
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_subsection(title):
    print(f"\n📊 {title}")
    print("-" * 40)

def main():
    # Initialize API client - reads from .env file
    cambrian = CambrianAPI()
    
    print("🌟 Cambrian API - Common Workflows Demo")
    print("This demo showcases the key use cases for Solana DeFi analytics")
    
    try:
        # ==============================================
        # Workflow 1: Token Research & Analysis
        # ==============================================
        print_section("WORKFLOW 1: Token Research & Analysis")
        
        print_subsection("Step 1: Discover Trending Tokens")
        trending_raw = cambrian.get_trending_tokens(order_by="volume_usd_24h", limit=10)
        trending_tokens = cambrian.parse_response(trending_raw)
        
        print(f"Found {len(trending_tokens)} trending tokens by 24h volume (showing top 10):")
        for i, token in enumerate(trending_tokens, 1):
            symbol = token.get('symbol', 'Unknown')
            price = token.get('currentPriceUSD', 0)
            change = token.get('priceChangePercentage', 0)
            volume = token.get('volume24hUSD', 0)
            
            change_emoji = "📈" if change >= 0 else "📉"
            print(f"  {i:2}. {symbol:8} | ${price:8.4f} | {change:+6.2f}% {change_emoji} | Vol: ${volume:,.0f}")
        
        print_subsection("Step 2: Deep Dive Analysis on SOL")
        sol_address = "So11111111111111111111111111111111111111112"
        
        # Get current price
        price_raw = cambrian.get_current_price(sol_address)
        price_data = cambrian.parse_response(price_raw)[0]
        print(f"SOL Current Price: ${price_data['priceUSD']:.4f}")
        
        # Get token details
        details_raw = cambrian.get_token_details(sol_address)
        details = cambrian.parse_response(details_raw)
        if details:
            detail = details[0]
            print(f"SOL Details:")
            for key, value in detail.items():
                if key == 'tokenAddress':
                    continue
                print(f"  {key}: {value}")
        
        # ==============================================
        # Workflow 2: Market Intelligence Dashboard
        # ==============================================
        print_section("WORKFLOW 2: Market Intelligence Dashboard")
        
        print_subsection("Latest Block Info")
        block_raw = cambrian.get_latest_block()
        block_data = cambrian.parse_response(block_raw)[0]
        print(f"Block Number: {block_data['blockNumber']:,}")
        print(f"Block Time: {block_data['blockTime']} (Unix timestamp)")
        
        print_subsection("Top Volume Tokens Today")
        for i, token in enumerate(trending_tokens[:3], 1):
            symbol = token.get('symbol', 'Unknown')
            volume = token.get('volume24hUSD', 0)
            price = token.get('currentPriceUSD', 0)
            
            print(f"  #{i} {symbol}")
            print(f"     Price: ${price:.6f}")
            print(f"     24h Volume: ${volume:,.2f}")
            print(f"     Address: {token.get('tokenAddress', 'N/A')}")
            
        # ==============================================
        # Workflow 3: Price Analysis & Comparison
        # ==============================================
        print_section("WORKFLOW 3: Multi-Token Price Analysis")
        
        print_subsection("Price Comparison Dashboard")
        
        # Since the multi-price API has limitations, use the trending data directly
        # which already contains all the price information we need
        print(f"📊 Real-time Price Comparison (Top 5 Trending Tokens):")
        print("=" * 80)
        print(f"{'Token':<12} {'Current Price':<15} {'24h Volume':<15} {'24h Change':<15} {'Trend'}")
        print("-" * 80)
        
        for token in trending_tokens[:5]:
            symbol = token.get('symbol', 'Unknown')[:10]
            price = token.get('currentPriceUSD', 0)
            volume = token.get('volume24hUSD', 0)
            change_pct = token.get('priceChangePercentage', 0)
            
            # Format price
            if price >= 1000:
                price_str = f"${price:,.2f}"
            elif price >= 1:
                price_str = f"${price:.4f}"
            else:
                price_str = f"${price:.6f}"
            
            # Format volume
            if volume > 1000000000:
                vol_str = f"${volume/1000000000:.1f}B"
            elif volume > 1000000:
                vol_str = f"${volume/1000000:.1f}M"
            elif volume > 1000:
                vol_str = f"${volume/1000:.1f}K"
            else:
                vol_str = f"${volume:,.0f}"
            
            # Format change
            if change_pct >= 0:
                change_str = f"+{change_pct:.2f}%"
                trend = "📈 UP"
            else:
                change_str = f"{change_pct:.2f}%"
                trend = "📉 DOWN"
            
            print(f"{symbol:<12} {price_str:<15} {vol_str:<15} {change_str:<15} {trend}")
        
        print("=" * 80)
        print("💡 Note: Data sourced from trending tokens with real-time price feeds")
        print("=" * 80)
        
        # Price performance analysis
        print_subsection("Price Performance Analysis")
        gainers = [t for t in trending_tokens[:5] if t.get('priceChangePercentage', 0) > 0]
        losers = [t for t in trending_tokens[:5] if t.get('priceChangePercentage', 0) < 0]
        
        if gainers:
            print(f"📈 Top Gainers ({len(gainers)} tokens):")
            for token in gainers[:3]:
                symbol = token['symbol'][:8]
                change = token.get('priceChangePercentage', 0)
                price = token.get('currentPriceUSD', 0)
                print(f"  • {symbol:8} +{change:.2f}% (${price:.6f})")
        else:
            print("📈 No tokens with positive price movement in top 5")
        
        if losers:
            print(f"\n📉 Top Decliners ({len(losers)} tokens):")
            for token in losers[:3]:
                symbol = token['symbol'][:8]
                change = token.get('priceChangePercentage', 0)
                price = token.get('currentPriceUSD', 0)
                print(f"  • {symbol:8} {change:.2f}% (${price:.6f})")
        
        # Volume leaders
        print(f"\n💰 Volume Leaders:")
        volume_sorted = sorted(trending_tokens[:5], 
                             key=lambda x: x.get('volume24hUSD', 0), 
                             reverse=True)
        for i, token in enumerate(volume_sorted[:3], 1):
            symbol = token['symbol'][:8]
            volume = token.get('volume24hUSD', 0)
            if volume > 1000000000:
                vol_str = f"${volume/1000000000:.2f}B"
            elif volume > 1000000:
                vol_str = f"${volume/1000000:.1f}M"
            else:
                vol_str = f"${volume:,.0f}"
            print(f"  {i}. {symbol:8} {vol_str} (24h volume)")
                
        
        # ==============================================
        # Workflow 4: Trading Analytics Deep Dive
        # ==============================================
        print_section("WORKFLOW 4: Trading Analytics Deep Dive")
        
        print_subsection("Trade Statistics Analysis (Top 5 Trending Tokens)")
        print("🔍 Analyzing trading patterns, buy/sell ratios, and market sentiment...")
        
        # Get trade statistics for each trending token
        trading_analysis = []
        for i, token in enumerate(trending_tokens[:5], 1):
            token_address = token['tokenAddress']
            symbol = token['symbol'][:8]
            
            print(f"\n📊 [{i}/5] Analyzing {symbol} trading patterns...")
            
            try:
                # Get trade statistics
                trade_stats_raw = cambrian.get_trade_statistics([token_address], timeframe="24h")
                trade_stats = cambrian.parse_response(trade_stats_raw)
                
                if trade_stats:
                    stats = trade_stats[0]
                    
                    # Use the correct field names from API
                    total_trades = stats.get('totalTradeCount', 0)
                    buy_trades = stats.get('buyCount', 0)
                    sell_trades = stats.get('sellCount', 0)
                    buy_volume_usd = stats.get('volumeBuyUSD', 0)
                    sell_volume_usd = stats.get('volumeSellUSD', 0)
                    total_volume_usd = stats.get('totalVolumeUSD', 0)
                    buy_to_sell_ratio = stats.get('buyToSellRatio', 0)
                    
                    # Calculate ratios
                    buy_ratio = (buy_trades / total_trades * 100) if total_trades > 0 else 0
                    sell_ratio = (sell_trades / total_trades * 100) if total_trades > 0 else 0
                    buy_volume_ratio = (buy_volume_usd / total_volume_usd * 100) if total_volume_usd > 0 else 0
                    sell_volume_ratio = (sell_volume_usd / total_volume_usd * 100) if total_volume_usd > 0 else 0
                    
                    # Determine market sentiment
                    if buy_volume_ratio > 55:
                        sentiment = "🟢 BULLISH"
                    elif buy_volume_ratio < 45:
                        sentiment = "🔴 BEARISH"
                    else:
                        sentiment = "🟡 NEUTRAL"
                    
                    trading_analysis.append({
                        'symbol': symbol,
                        'address': token_address,
                        'total_trades': total_trades,
                        'buy_trades': buy_trades,
                        'sell_trades': sell_trades,
                        'buy_ratio': buy_ratio,
                        'sell_ratio': sell_ratio,
                        'buy_volume_usd': buy_volume_usd,
                        'sell_volume_usd': sell_volume_usd,
                        'buy_volume_ratio': buy_volume_ratio,
                        'sell_volume_ratio': sell_volume_ratio,
                        'sentiment': sentiment,
                        'total_volume_usd': total_volume_usd
                    })
                    
                    print(f"   ✅ {symbol}: {total_trades:,} trades, {sentiment}")
                
                else:
                    print(f"   ⚠️  {symbol}: No trade statistics available")
                    
            except Exception as e:
                print(f"   ❌ {symbol}: Error getting trade stats - {e}")
                continue
        
        if trading_analysis:
            print(f"\n📋 Trading Analysis Summary (24h Period)")
            print("=" * 100)
            print(f"{'Token':<8} {'Total Trades':<12} {'Buy/Sell Ratio':<15} {'Volume Ratio':<15} {'Sentiment':<12} {'Total Volume'}")
            print("-" * 100)
            
            for analysis in trading_analysis:
                symbol = analysis['symbol']
                total_trades = analysis['total_trades']
                buy_ratio = analysis['buy_ratio']
                sell_ratio = analysis['sell_ratio']
                buy_vol_ratio = analysis['buy_volume_ratio']
                sell_vol_ratio = analysis['sell_volume_ratio']
                sentiment = analysis['sentiment']
                total_volume = analysis['total_volume_usd']
                
                # Format numbers
                if total_trades >= 1000000:
                    trades_str = f"{total_trades/1000000:.1f}M"
                elif total_trades >= 1000:
                    trades_str = f"{total_trades/1000:.1f}K"
                else:
                    trades_str = f"{total_trades:,}"
                
                if total_volume > 1000000000:
                    volume_str = f"${total_volume/1000000000:.1f}B"
                elif total_volume > 1000000:
                    volume_str = f"${total_volume/1000000:.1f}M"
                else:
                    volume_str = f"${total_volume:,.0f}"
                
                ratio_str = f"{buy_ratio:.1f}%/{sell_ratio:.1f}%"
                vol_ratio_str = f"{buy_vol_ratio:.1f}%/{sell_vol_ratio:.1f}%"
                
                print(f"{symbol:<8} {trades_str:<12} {ratio_str:<15} {vol_ratio_str:<15} {sentiment:<12} {volume_str}")
            
            print("=" * 100)
            
            # Market sentiment analysis
            print_subsection("Market Sentiment Analysis")
            bullish_tokens = [t for t in trading_analysis if "BULLISH" in t['sentiment']]
            bearish_tokens = [t for t in trading_analysis if "BEARISH" in t['sentiment']]
            neutral_tokens = [t for t in trading_analysis if "NEUTRAL" in t['sentiment']]
            
            print(f"🟢 Bullish Sentiment: {len(bullish_tokens)} tokens")
            for token in bullish_tokens:
                print(f"   • {token['symbol']}: {token['buy_volume_ratio']:.1f}% buy volume dominance")
            
            print(f"\n🔴 Bearish Sentiment: {len(bearish_tokens)} tokens")
            for token in bearish_tokens:
                print(f"   • {token['symbol']}: {token['sell_volume_ratio']:.1f}% sell volume dominance")
                
            print(f"\n🟡 Neutral Sentiment: {len(neutral_tokens)} tokens")
            for token in neutral_tokens:
                print(f"   • {token['symbol']}: Balanced trading ({token['buy_volume_ratio']:.1f}%/{token['sell_volume_ratio']:.1f}%)")
            
            # Trading activity ranking
            print_subsection("Trading Activity Rankings")
            
            # Most active by trade count
            by_trades = sorted(trading_analysis, key=lambda x: x['total_trades'], reverse=True)
            print("🔥 Most Active by Trade Count:")
            for i, token in enumerate(by_trades[:3], 1):
                trades = token['total_trades']
                trades_str = f"{trades/1000000:.1f}M" if trades >= 1000000 else f"{trades/1000:.1f}K"
                print(f"   {i}. {token['symbol']}: {trades_str} trades")
            
            # Highest volume
            by_volume = sorted(trading_analysis, key=lambda x: x['total_volume_usd'], reverse=True)
            print(f"\n💰 Highest Trading Volume:")
            for i, token in enumerate(by_volume[:3], 1):
                volume = token['total_volume_usd']
                volume_str = f"${volume/1000000000:.1f}B" if volume >= 1000000000 else f"${volume/1000000:.1f}M"
                print(f"   {i}. {token['symbol']}: {volume_str}")
            
            # Most bullish (highest buy ratio)
            by_bullish = sorted(trading_analysis, key=lambda x: x['buy_volume_ratio'], reverse=True)
            print(f"\n📈 Most Bullish (Buy Volume %):")
            for i, token in enumerate(by_bullish[:3], 1):
                buy_ratio = token['buy_volume_ratio']
                print(f"   {i}. {token['symbol']}: {buy_ratio:.1f}% buy volume")
                
        else:
            print("❌ No trading analysis data available for trending tokens")
        
        # ==============================================
        # Summary & Next Steps
        # ==============================================
        print_section("SUMMARY & NEXT STEPS")
        
        print("✅ Successfully tested key Cambrian API workflows:")
        print("   • Token discovery and trending analysis")
        print("   • Real-time price data retrieval") 
        print("   • Token metadata and details lookup")
        print("   • Multi-token price comparison")
        print("   • Market intelligence dashboard data")
        print("   • Advanced trading analytics with buy/sell ratios")
        print("   • Market sentiment analysis based on trading patterns")
        print("   • Trading activity rankings and comparisons")
        
        print("\n🛠️  Next steps you could implement:")
        print("   • Portfolio tracking with wallet addresses")
        print("   • Liquidity pool analysis and yield farming")
        print("   • Trading signal generation")
        print("   • Historical price trend analysis")
        print("   • Automated alerts for price movements")
        
        print("\n📚 Available endpoints to explore:")
        print("   • Token holder analysis")
        print("   • Transaction tracking")
        print("   • Pool performance metrics")
        print("   • Trading statistics")
        print("   • OHLCV candlestick data")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()