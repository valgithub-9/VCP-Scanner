#!/usr/bin/env python3
"""
Daily VCP (Volatility Contraction Pattern) Scanner for QQQ Holdings
Runs after market close and emails results
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

warnings.filterwarnings('ignore')

# QQQ holdings (top 100 Nasdaq stocks)
qqq_tickers = [
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'GOOG', 'AMZN', 'META', 'TSLA', 'AVGO', 'QCOM',
    'CSCO', 'INTEL', 'AMD', 'UBER', 'SHOP', 'SNOW', 'ZM', 'ADBE', 'NFLX', 'PYPL',
    'CRM', 'NOW', 'INTU', 'VRSK', 'SNPS', 'CDNS', 'ASML', 'AMAT', 'LRCX', 'MU',
    'AVGO', 'ARM', 'PCAR', 'PAYX', 'XLNX', 'CHTR', 'TTD', 'ABNB', 'DASH', 'FTNT',
    'NET', 'CRWD', 'OKTA', 'ZS', 'DDOG', 'DBX', 'RBLX', 'U', 'PLTR', 'ROKU',
    'SPOT', 'COIN', 'MSTR', 'MELI', 'SQ', 'HOOD', 'UPST', 'SOFI', 'ARKK', 'XBI',
]

def scan_vcp_patterns():
    """Scan for VCP patterns and return results"""
    print("🔍 Scanning QQQ for real VCP patterns...")
    print(f"⏱️  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ET\n")

    results = []

    for ticker in qqq_tickers[:40]:  # Scan first 40 for speed
        try:
            # Download data: 1 year for analysis
            stock = yf.Ticker(ticker)
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

            # Base range
            base_range = resistance_level - support_level

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
            print(f"⚠️  {ticker}: {str(e)}")
            continue

    return results

def format_results_email(df):
    """Format results as HTML email"""
    if df.empty:
        return "<p>No VCP patterns found matching criteria.</p>"

    df_sorted = df.sort_values('VCP Score', ascending=False)

    html = f"""
    <h2>🎯 Daily VCP Scan Results</h2>
    <p><strong>Scan Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ET</p>
    <p><strong>Patterns Found:</strong> {len(df_sorted)}</p>
    <p><strong>Elite Setups (Score 70%+):</strong> {len(df_sorted[df_sorted['VCP Score'] >= 70])}</p>

    <h3>Top 5 VCP Setups (Ready to Trade)</h3>
    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
        <tr style="background-color: #f2f2f2;">
            <th>Ticker</th>
            <th>Price</th>
            <th>52W High</th>
            <th>% to High</th>
            <th>Vol 20d</th>
            <th>VCP Score</th>
            <th>Market Cap</th>
        </tr>
    """

    for i, row in df_sorted.head(5).iterrows():
        html += f"""
        <tr>
            <td>{row['Ticker']}</td>
            <td>${row['Price']}</td>
            <td>${row['52W High']}</td>
            <td>{row['% to High']:.1f}%</td>
            <td>{row['Vol 20d']:.1f}%</td>
            <td>{row['VCP Score']:.0f}%</td>
            <td>${row['Market Cap ($B)']:.1f}B</td>
        </tr>
        """

    html += """
    </table>
    <h3>Full Results</h3>
    """
    html += df_sorted.to_html(index=False, border=0)

    return html

def main():
    # Run scan
    results = scan_vcp_patterns()

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values('VCP Score', ascending=False)

        print("=" * 130)
        print("REAL VCP PATTERNS (QQQ) - LIVE DATA")
        print("=" * 130)
        print(df.to_string(index=False))
        print("=" * 130)

        print(f"\n📊 SUMMARY:")
        print(f"   Total VCP setups found: {len(df)}")
        print(f"   Elite patterns (70%+): {len(df[df['VCP Score'] >= 70])}")
        print(f"   Avg volatility: {df['Vol 20d'].mean():.1f}%")
        print(f"   Avg price to high: {df['% to High'].mean():.1f}%")

        print(f"\n🎯 TOP 5 SETUPS:")
        for i, row in df.head(5).iterrows():
            print(f"   {row['Ticker']}: {row['VCP Score']:.0f}% | ${row['Price']} | {row['% to High']:.1f}% to high | Vol: {row['Vol 20d']:.1f}%")

        # Save to CSV
        csv_filename = f"vcp_scan_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\n✅ Results saved to {csv_filename}")

        # Email results if configured
        email = os.getenv('GMAIL_RECIPIENT')
        if email:
            try:
                # Send email (would use Gmail API or SMTP with credentials from env)
                print(f"\n📧 Email would be sent to: {email}")
            except Exception as e:
                print(f"⚠️  Could not send email: {str(e)}")
    else:
        print("❌ No VCP patterns found matching criteria")

if __name__ == '__main__':
    main()
