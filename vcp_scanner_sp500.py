#!/usr/bin/env python3
"""
S&P 500 VCP Pattern Scanner
Scans the S&P 500 for Volatility Contraction Patterns
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Top 100 S&P 500 stocks (by market cap)
sp500_tickers = [
    'MSFT', 'AAPL', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'BERKB', 'AVGO', 'QCOM',
    'AMD', 'CRM', 'MU', 'NFLX', 'ADBE', 'INTC', 'NOW', 'IBM', 'INTU', 'CSCO',
    'ASML', 'TXN', 'SNOW', 'AMAT', 'KLAC', 'SNPS', 'CDNS', 'MXIM', 'PYPL', 'VRSK',
    'SQ', 'TTD', 'PSTG', 'NXPI', 'SHOP', 'PANW', 'CRWD', 'NET', 'DDOG', 'ABNB',
    'DBX', 'DECK', 'PINS', 'DASH', 'COIN', 'ZS', 'OKTA', 'ZM', 'UPST', 'RBLX',
    'U', 'ROKU', 'SPOT', 'ARM', 'MSTR', 'PLTR', 'HOOD', 'SOFI', 'TPG', 'BLK',
    'GS', 'JPM', 'BAC', 'WFC', 'C', 'USB', 'PNC', 'TFC', 'RF', 'KEY',
    'UNH', 'LLY', 'JNJ', 'MRK', 'PFE', 'ABBV', 'AMGN', 'GILD', 'CDNA', 'AXON',
    'XOM', 'CVX', 'COP', 'EOG', 'MPC', 'PSX', 'FANG', 'OXY', 'HES', 'DVN',
    'MCD', 'YUM', 'SBUX', 'NKE', 'LULU', 'ULTA', 'OLAPF', 'APP', 'VITX', 'MKTX',
]

def scan_vcp_sp500():
    """Scan S&P 500 for VCP patterns"""
    print("🔍 Scanning S&P 500 for VCP patterns...")
    print(f"⏱️  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ET\n")

    results = []
    failed = []

    for i, ticker in enumerate(sp500_tickers, 1):
        print(f"   [{i}/{len(sp500_tickers)}] Scanning {ticker}...", end='\r')

        try:
            # Download data: 1 year for analysis
            hist = yf.download(ticker, period='1y', progress=False)

            if len(hist) < 100:
                continue

            # Current metrics
            current_price = hist['Close'].iloc[-1]
            high_52w = hist['High'].tail(252).max() if len(hist) >= 252 else hist['High'].max()

            # Distance to 52W high
            dist_to_high = ((high_52w - current_price) / high_52w) * 100

            # Volatility (last 20 days)
            returns_20d = hist['Close'].pct_change().tail(20)
            vol_20d = returns_20d.std() * np.sqrt(252) * 100

            # Volatility (last 90 days) for comparison
            returns_90d = hist['Close'].pct_change().tail(90)
            vol_90d = returns_90d.std() * np.sqrt(252) * 100

            # Is volatility contracting?
            vol_contraction = vol_20d < (vol_90d * 0.7)

            # Support levels (last 50 days)
            recent_50d = hist['Close'].tail(50)
            support_level = recent_50d.min()
            resistance_level = recent_50d.max()

            # Prior run-up
            price_3m_ago = hist['Close'].iloc[-90] if len(hist) >= 90 else hist['Close'].iloc[0]
            prior_runup = ((resistance_level - price_3m_ago) / price_3m_ago) * 100 if price_3m_ago > 0 else 0

            # VCP Strength Score
            strength = 0

            if vol_20d < 8:
                strength += 35
            elif vol_20d < 10:
                strength += 25
            elif vol_20d < 12:
                strength += 15

            if dist_to_high < 5:
                strength += 25
            elif dist_to_high < 10:
                strength += 20
            elif dist_to_high < 15:
                strength += 10

            dist_to_support = ((current_price - support_level) / support_level) * 100
            if dist_to_support < 5:
                strength += 20
            elif dist_to_support < 10:
                strength += 15

            if prior_runup >= 30 and prior_runup <= 80:
                strength += 25

            strength = min(100, strength)

            # Filter: Only include if reasonable VCP candidate
            if (vol_contraction and dist_to_high < 15 and strength >= 45):
                try:
                    stock = yf.Ticker(ticker)
                    market_cap = stock.info.get('marketCap', 0) / 1e9
                except:
                    market_cap = 0

                results.append({
                    'Ticker': ticker,
                    'Price': round(current_price, 2),
                    '52W High': round(high_52w, 2),
                    '% to High': round(dist_to_high, 1),
                    'Vol 20d': round(vol_20d, 1),
                    'Vol 90d': round(vol_90d, 1),
                    'Contraction': 'YES' if vol_contraction else 'NO',
                    'Prior Runup %': round(prior_runup, 1),
                    'Support': round(support_level, 2),
                    'Resistance': round(resistance_level, 2),
                    'VCP Score': round(strength, 0),
                    'Market Cap ($B)': round(market_cap, 1),
                })

        except Exception as e:
            failed.append((ticker, str(e)))
            continue

    print(" " * 60)
    return results, failed

def main():
    # Run scan
    results, failed = scan_vcp_sp500()

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values('VCP Score', ascending=False)

        print("\n" + "=" * 150)
        print("🎯 S&P 500 VCP PATTERNS - LIVE DATA")
        print("=" * 150)
        print(df.to_string(index=False))
        print("=" * 150)

        print(f"\n📊 SUMMARY:")
        print(f"   Total VCP setups found: {len(df)}")
        print(f"   Elite patterns (70%+): {len(df[df['VCP Score'] >= 70])}")
        print(f"   High quality patterns (60-70%): {len(df[(df['VCP Score'] >= 60) & (df['VCP Score'] < 70)])}")
        print(f"   Avg volatility: {df['Vol 20d'].mean():.1f}%")
        print(f"   Avg price to high: {df['% to High'].mean():.1f}%")

        print(f"\n🏆 TOP 10 SETUPS:")
        for i, row in df.head(10).iterrows():
            print(f"   {row['Ticker']}: {row['VCP Score']:.0f}% | ${row['Price']} | {row['% to High']:.1f}% to high | Vol: {row['Vol 20d']:.1f}%")

        # Save to CSV
        csv_filename = f"vcp_scan_sp500_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\n✅ Results saved to {csv_filename}")

        # Get AI analysis
        print(f"\n💡 Want AI analysis? Run:")
        print(f"   python ai_finance_agent.py --analyze")

    else:
        print("❌ No VCP patterns found matching criteria")

    if failed:
        print(f"\n⚠️  Failed to fetch data for {len(failed)} tickers")

if __name__ == '__main__':
    main()
