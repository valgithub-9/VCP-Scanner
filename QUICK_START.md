# Quick Start Guide - AI Finance Agent

Get started in 5 minutes!

## Installation (Choose Your OS)

### macOS/Linux
```bash
# Clone and setup
git clone https://github.com/valgithub-9/vcp-scanner.git
cd vcp-scanner
bash setup.sh

# Edit .env with your API key
nano .env
```

### Windows
```cmd
# Clone and setup
git clone https://github.com/valgithub-9/vcp-scanner.git
cd vcp-scanner
setup.bat

# Edit .env with your API key
notepad .env
```

## Getting Your API Key

1. Go to https://console.anthropic.com/account/keys
2. Click "Create Key"
3. Copy the key and paste it into `.env` file:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

## Running the Tools

### Activate Environment (Always first)

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

### Run VCP Scanner Only
```bash
python vcp_scanner.py
```

**Output:** 
- Prints results to terminal
- Saves CSV: `vcp_scan_20240807.csv`

### Run AI Finance Agent (Interactive)
```bash
python ai_finance_agent.py
```

**Example conversation:**
```
Agent: Hello! I'm your AI Finance Agent...

You: What are the top VCP setups today?
Agent: Based on today's scan, here are the best setups...

You: Analyze NVDA for me
Agent: NVDA shows interesting technical setup...

You: quit
Agent: Goodbye!
```

### Analyze VCP Results with AI
```bash
python ai_finance_agent.py --analyze
```

**Output:** AI analysis of today's scan results

### Analyze Specific Stock
```bash
python ai_finance_agent.py --analyze-ticker AAPL
```

**Output:** Trading insights for AAPL

## Common Commands Cheat Sheet

| Command | Purpose |
|---------|---------|
| `python vcp_scanner.py` | Run VCP scan |
| `python ai_finance_agent.py` | Start interactive AI chat |
| `python ai_finance_agent.py --analyze` | Analyze scan results |
| `python ai_finance_agent.py --analyze-ticker TSLA` | Get insights for TSLA |
| `pip list` | Show installed packages |
| `pip install -r requirements.txt` | Install/update dependencies |

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
**Solution:** Make sure you added the key to `.env` file

### "No module named 'anthropic'"
**Solution:** Run `pip install -r requirements.txt`

### "Network error connecting to API"
**Solution:** Check internet connection, verify API key is valid

### "No VCP patterns found"
**Solution:** Markets might be down, try again after hours

## What's Next?

1. ✅ Run your first scan: `python vcp_scanner.py`
2. ✅ Chat with AI: `python ai_finance_agent.py`
3. ✅ Analyze results: `python ai_finance_agent.py --analyze`
4. 📚 Read full docs: See [INSTALL.md](INSTALL.md)
5. ⏰ Schedule daily scans: See [INSTALL.md](INSTALL.md#schedule-daily-scans)

## Example Session

```bash
$ source venv/bin/activate
$ python vcp_scanner.py
🔍 Scanning QQQ for real VCP patterns...
⏱️  2024-08-07 16:30:00 ET

================================================================================
REAL VCP PATTERNS (QQQ) - LIVE DATA
================================================================================
   Ticker  Price  52W High  % to High  Vol 20d  Contraction  VCP Score
     AAPL  225.43    235.67        4.3%     12.5          YES         78
     MSFT  420.12    445.23        5.6%     11.2          YES         72

$ python ai_finance_agent.py --analyze

Agent: Based on today's VCP scan results, here are my top recommendations...
```

## Support

- 📖 Full docs: [INSTALL.md](INSTALL.md)
- 🐛 Issues: Check troubleshooting section
- 💡 Ideas: Open an issue on GitHub

---

**Ready to trade?** You're all set! Start with `python ai_finance_agent.py` 🚀
