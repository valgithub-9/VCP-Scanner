# VCP-Scanner with AI Finance Agent

A powerful stock analysis tool that combines **Volatility Contraction Pattern (VCP) scanning** with **AI-powered trading insights** using Claude AI.

## Features

### 📊 VCP Scanner
- Scans QQQ holdings (40+ tech stocks) daily for VCP patterns
- Analyzes volatility contraction, support/resistance levels
- Generates VCP strength scores (0-100%)
- Exports results to CSV for record-keeping
- Email alert integration (optional)

### 🤖 AI Finance Agent
- **Intelligent Pattern Recognition**: Claude AI analyzes technical patterns
- **Interactive Chat**: Multi-turn conversations with your AI advisor
- **Real-time Analysis**: Analyze any ticker for trading insights
- **VCP Result Analysis**: Get AI recommendations on scan results
- **Risk Management**: AI-suggested position sizing and risk/reward ratios

## Quick Start

### 1. Install

```bash
# Clone repository
git clone https://github.com/valgithub-9/vcp-scanner.git
cd vcp-scanner

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

Get your API key from [Anthropic Console](https://console.anthropic.com/account/keys)

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or create a `.env` file:

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run

```bash
# Run VCP Scanner
python vcp_scanner.py

# Run AI Finance Agent (interactive)
python ai_finance_agent.py

# Analyze specific ticker
python ai_finance_agent.py --analyze-ticker AAPL

# Analyze VCP scan results
python ai_finance_agent.py --analyze
```

## Usage Examples

### Interactive Chat with AI Agent

```bash
$ python ai_finance_agent.py
🤖 AI Finance Agent - Interactive Mode

Agent: Hello! I'm your AI Finance Agent...

You: What's the setup for NVDA right now?
Agent: Based on current technical analysis, NVDA shows...
```

### Analyze VCP Scan Results

```bash
$ python ai_finance_agent.py --analyze
📊 Analyzing VCP scan results...
Agent: Based on today's VCP scan, the top 3 setups are...
```

### Analyze Specific Stock

```bash
$ python ai_finance_agent.py --analyze-ticker MSFT
📈 Analyzing MSFT...
Agent: MSFT is currently trading near...
```

## Complete Installation Guide

For detailed setup instructions, see [INSTALL.md](INSTALL.md)

## Project Structure

```
vcp-scanner/
├── vcp_scanner.py           # VCP pattern scanner
├── ai_finance_agent.py      # AI finance agent with Claude
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── INSTALL.md              # Detailed installation guide
├── .env.example            # Environment variables template
└── .gitignore              # Git ignore file
```

## Requirements

- Python 3.8+
- Anthropic API key (free tier available)
- Internet connection for market data

## API Costs

- **Anthropic Claude API**: Pay-as-you-go pricing (~$0.003 per 1K input tokens)
- **yfinance**: Free stock data
- **Gmail**: Free (if using email alerts)

## Disclaimer

This tool is for educational and research purposes only. Not financial advice. Always do your own due diligence before trading. Past performance does not guarantee future results.

## Support & Issues

See [INSTALL.md](INSTALL.md) for troubleshooting guides.

## License

MIT License - See project repository for details.
