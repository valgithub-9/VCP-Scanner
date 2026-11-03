# AI Finance Agent Installation Guide

This guide covers the installation and setup of the AI Finance Agent for the VCP Scanner.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/valgithub-9/vcp-scanner.git
cd vcp-scanner
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

#### For Claude AI Finance Agent:

Set your Anthropic API key:

```bash
# On macOS/Linux
export ANTHROPIC_API_KEY="your-api-key-here"

# On Windows (Command Prompt)
set ANTHROPIC_API_KEY=your-api-key-here

# On Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your-api-key-here
GMAIL_RECIPIENT=your-email@gmail.com
```

#### For Email Notifications (Optional):

```bash
export GMAIL_RECIPIENT="your-email@gmail.com"
```

### 5. Verify Installation

```bash
python -c "import anthropic; print('✅ Anthropic SDK installed successfully')"
python vcp_scanner.py
```

## Features

### VCP Scanner
- Scans QQQ holdings for Volatility Contraction Patterns (VCP)
- Analyzes 40+ tech stocks daily
- Generates VCP strength scores
- Exports results to CSV

### AI Finance Agent
- Real-time stock analysis using Claude AI
- Intelligent pattern recognition
- Trading insights and recommendations
- Email alert integration

## Usage

### Run VCP Scanner Only

```bash
python vcp_scanner.py
```

### Run with AI Finance Agent

```bash
python ai_finance_agent.py
```

### Schedule Daily Scans (Linux/macOS)

Add to crontab to run after market close (4 PM ET):

```bash
crontab -e
```

Add this line:

```
0 16 * * 1-5 cd /path/to/vcp-scanner && source venv/bin/activate && python vcp_scanner.py
```

## Project Structure

```
vcp-scanner/
├── vcp_scanner.py          # VCP pattern scanner
├── ai_finance_agent.py     # AI finance agent with Claude API
├── requirements.txt        # Python dependencies
├── README.md              # Project overview
├── INSTALL.md             # This file
└── .env.example           # Environment variables template
```

## Troubleshooting

### Import Error: No module named 'anthropic'

```bash
pip install --upgrade anthropic
```

### API Key Not Recognized

Verify your API key:

```bash
echo $ANTHROPIC_API_KEY
```

Ensure no spaces or quotes in the key.

### Financial Data Not Loading

The scanner uses yfinance to fetch stock data. Ensure you have internet connectivity:

```bash
python -c "import yfinance as yf; print(yf.Ticker('AAPL').info['symbol'])"
```

### Email Configuration Issues

Check that `GMAIL_RECIPIENT` environment variable is set:

```bash
echo $GMAIL_RECIPIENT
```

## API Rate Limits

- **Anthropic Claude**: 50,000 tokens/minute (free tier)
- **yfinance**: ~2000 requests/hour per IP
- **Gmail API**: 10M+ emails/day

## Security Best Practices

1. Never commit `.env` files with actual API keys
2. Use separate API keys for development and production
3. Rotate API keys regularly
4. Monitor API usage on your Anthropic dashboard

## Support

For issues or questions:
- Check the README.md for project overview
- Review error messages carefully
- Ensure all dependencies are installed: `pip list`

## Next Steps

1. Run the VCP Scanner: `python vcp_scanner.py`
2. Explore AI Finance Agent capabilities: `python ai_finance_agent.py`
3. Set up automated scheduling for production use
