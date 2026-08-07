#!/usr/bin/env python3
"""
AI Finance Agent - Claude-powered stock analysis and trading insights
Integrates with VCP Scanner to provide intelligent financial recommendations
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

try:
    from anthropic import Anthropic
except ImportError:
    print("❌ Error: anthropic package not installed")
    print("Install it with: pip install anthropic")
    sys.exit(1)

class AIFinanceAgent:
    """AI-powered finance agent using Claude API"""

    def __init__(self):
        """Initialize the AI Finance Agent"""
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Set it or add to .env file"
            )

        self.client = Anthropic()
        self.conversation_history = []
        self.model = "claude-3-5-sonnet-20241022"

        # System prompt for finance expertise
        self.system_prompt = """You are an expert financial analyst and trading advisor with deep knowledge of:
- Technical analysis and chart patterns (especially Volatility Contraction Patterns)
- Fundamental stock analysis
- Risk management and position sizing
- Market psychology and trading psychology
- Options strategies
- Portfolio management

Your role is to:
1. Analyze VCP scan results and provide trading insights
2. Identify high-probability trading setups
3. Suggest risk/reward ratios and entry/exit points
4. Explain technical patterns in simple terms
5. Provide actionable trading recommendations

Always:
- Be specific with numbers and percentages
- Explain your reasoning clearly
- Consider risk management in recommendations
- Acknowledge uncertainty and market conditions
- Suggest position sizes as percentages of portfolio"""

    def get_stock_info(self, ticker: str) -> dict:
        """Fetch current stock information"""
        try:
            stock = yf.Ticker(ticker)
            hist = yf.download(ticker, period='3mo', progress=False)

            if len(hist) < 2:
                return None

            return {
                'ticker': ticker,
                'price': hist['Close'].iloc[-1],
                'previous_close': hist['Close'].iloc[-2],
                'high_52w': hist['High'].max(),
                'low_52w': hist['Low'].min(),
                'volume_avg': hist['Volume'].mean(),
                'volatility': hist['Close'].pct_change().std() * np.sqrt(252) * 100,
                'price_change_today': (
                    (hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) /
                    hist['Close'].iloc[-2] * 100
                ),
                'trend': 'UP' if hist['Close'].iloc[-1] > hist['Close'].iloc[-5] else 'DOWN'
            }
        except Exception as e:
            print(f"⚠️  Error fetching data for {ticker}: {e}")
            return None

    def analyze_vcp_results(self, csv_file: str = None) -> str:
        """Analyze VCP scan results using AI"""

        # Try to load scan results from CSV
        if csv_file and os.path.exists(csv_file):
            try:
                df = pd.read_csv(csv_file)
                scan_data = df.to_string()
            except Exception as e:
                print(f"⚠️  Could not read CSV file: {e}")
                scan_data = "VCP scan data not available"
        else:
            # Use recent scan results if available
            recent_csvs = [f for f in os.listdir('.') if f.startswith('vcp_scan_') and f.endswith('.csv')]
            if recent_csvs:
                latest_csv = sorted(recent_csvs)[-1]
                try:
                    df = pd.read_csv(latest_csv)
                    scan_data = df.to_string()
                except:
                    scan_data = "VCP scan data available but could not be read"
            else:
                scan_data = "No recent VCP scan results found"

        # Create analysis request
        prompt = f"""Here are today's VCP scan results for QQQ holdings:

{scan_data}

Please provide:
1. Top 3 trading setups ranked by probability of success
2. Risk/reward analysis for the top setup
3. Suggested entry and exit points for each top setup
4. Position sizing recommendation (% of portfolio)
5. Key risks to monitor
6. Overall market conditions assessment"""

        return self.chat(prompt)

    def get_trading_insight(self, ticker: str) -> str:
        """Get AI trading insight for a specific ticker"""
        stock_info = self.get_stock_info(ticker)

        if not stock_info:
            return f"Unable to fetch data for {ticker}"

        prompt = f"""Analyze this stock for trading opportunities:

Ticker: {ticker}
Current Price: ${stock_info['price']:.2f}
52-Week High: ${stock_info['high_52w']:.2f}
52-Week Low: ${stock_info['low_52w']:.2f}
Distance to 52W High: {((stock_info['high_52w'] - stock_info['price']) / stock_info['high_52w'] * 100):.1f}%
Annualized Volatility: {stock_info['volatility']:.1f}%
Trend: {stock_info['trend']}
Today's Change: {stock_info['price_change_today']:.2f}%

Provide:
1. Short-term trading outlook (1-5 days)
2. Technical setup assessment
3. Risk/reward for a long position from current levels
4. Suggested entry and stop loss levels"""

        return self.chat(prompt)

    def chat(self, user_message: str) -> str:
        """Send a message to Claude and get a response"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=self.system_prompt,
                messages=self.conversation_history
            )

            assistant_message = response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message
        except Exception as e:
            error_msg = f"❌ API Error: {str(e)}"
            print(error_msg)
            return error_msg

    def multi_turn_conversation(self) -> None:
        """Start an interactive multi-turn conversation with the AI"""
        print("\n" + "="*60)
        print("🤖 AI Finance Agent - Interactive Mode")
        print("="*60)
        print("Chat with your AI financial advisor (type 'quit' to exit)\n")

        initial_greeting = (
            "Hello! I'm your AI Finance Agent powered by Claude. "
            "I can help you analyze VCP scan results, provide trading insights, "
            "and discuss trading strategies. What would you like to know?"
        )
        print(f"Agent: {initial_greeting}\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Agent: Goodbye! Good luck with your trading!")
                    break

                if not user_input:
                    continue

                response = self.chat(user_input)
                print(f"\nAgent: {response}\n")

            except KeyboardInterrupt:
                print("\nAgent: Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}\n")

def main():
    """Main entry point"""
    try:
        # Initialize agent
        agent = AIFinanceAgent()
        print("✅ AI Finance Agent initialized successfully!\n")

        # Check for command-line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == '--analyze':
                # Analyze VCP results
                csv_file = sys.argv[2] if len(sys.argv) > 2 else None
                print("📊 Analyzing VCP scan results...\n")
                analysis = agent.analyze_vcp_results(csv_file)
                print(analysis)

            elif sys.argv[1] == '--analyze-ticker':
                # Analyze specific ticker
                if len(sys.argv) < 3:
                    print("Usage: python ai_finance_agent.py --analyze-ticker TICKER")
                    sys.exit(1)
                ticker = sys.argv[2].upper()
                print(f"📈 Analyzing {ticker}...\n")
                insight = agent.get_trading_insight(ticker)
                print(insight)
            else:
                print("Unknown argument. Starting interactive mode...")
                agent.multi_turn_conversation()
        else:
            # Start interactive chat
            agent.multi_turn_conversation()

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nTo fix this:")
        print("1. Get your API key from https://console.anthropic.com")
        print("2. Set ANTHROPIC_API_KEY environment variable:")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        print("3. Or create a .env file with: ANTHROPIC_API_KEY=your-key-here")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Fatal Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
