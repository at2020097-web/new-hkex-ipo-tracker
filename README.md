# HKEX IPO Tracker - Real-time Discord Notifications

An automated system that monitors HKEX announcements and sends detailed reports to Discord.

## Features

- 📊 **Real-time Monitoring**: Checks for new announcements every 15 minutes
- 🌏 **HKEX Integration**: Fetches data from Hong Kong Stock Exchange
- 💰 **HKD Currency**: All financial values in Hong Kong Dollars
- 📈 **Alpha Vantage API**: Enhanced financial data
- 📰 **News Scraping**: AAStocks, SCMP, Bloomberg integration
- 💬 **Discord Notifications**: Sends formatted alerts to your channel
- 🔁 **Duplicate Prevention**: Tracks processed announcements
- 🤖 **AI Controller**: Voice & text command assistant for system control

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Keys

#### Alpha Vantage (Free Tier)
- Sign up at: https://www.alphavantage.co/support/#api-key
- Free tier: 5 requests/minute, 500 requests/day

#### Discord Bot
1. Go to: https://discord.com/developers/applications
2. Create application → Bot → Copy Token
3. Get Channel ID: Enable Developer Mode in Discord, right-click channel → Copy ID

### 3. Configure Environment

Edit `config/.env` with your credentials:
```
# Alpha Vantage API
AV_API_KEY=XB0JCI0CQD80PYHE

# Discord Bot
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
```

### 4. Run the System

For a single check:
```bash
python app.py
```

For continuous monitoring:
```bash
python scheduler.py
```

### 5. Run the AI Controller

The AI Controller allows you to control the system via voice or text commands:

```bash
python run_ai_controller.py
```

Or use text commands directly:
```bash
python -c "from src.ai_controller import AIController; c = AIController(); print(c.process_command('time'))"
```

## AI Controller - Voice & Text Commands

The AI Controller supports the following command categories:

### System Information
- `cpu` - Check CPU usage
- `memory` - Check memory usage
- `disk` - Check disk space
- `network` - Check network info
- `ip` - Get your IP address
- `time` - Get current time
- `date` - Get current date
- `system info` - Full system information
- `battery` - Battery status
- `uptime` - System uptime

### File Operations
- `create file [name]` - Create a new file
- `read file [name]` - Read file contents
- `delete file [name]` - Delete a file
- `list files [folder]` - List files in directory
- `search files [keyword]` - Search for files
- `create folder [name]` - Create a new folder
- `copy [text]` - Copy text to clipboard
- `clipboard` - Read clipboard contents

### IPO System
- `run ipo` - Run IPO check now
- `send discord [message]` - Send to Discord
- `send whatsapp [message]` - Send to WhatsApp
- `check stock [code]` - Check stock info
- `stock price [code]` - Get real-time stock price
- `ipo history` - Show IPO history
- `clear ipo history` - Clear IPO history
- `get announcements` - Get latest HKEX announcements

### Web & Info
- `search [query]` - Web search
- `weather [city]` - Get weather
- `calculate [expr]` - Math calculation
- `joke` - Tell a joke
- `fact` - Random fact
- `open [website]` - Open a website
- `download [url]` - Download a file
- `translate [text] to [lang]` - Translate text

### Notes
- `note [text]` - Take a note
- `read notes` - Read your notes
- `clear notes` - Clear all notes

### Utilities
- `screenshot` - Take screenshot
- `processes` - List running processes
- `remind [text]` - Set a reminder
- `lock` - Lock the computer

### Development
- `git status` - Check git status
- `run script [name]` - Run a Python script

**Voice Commands**: Say "Hey AI" or "Computer" followed by your command to activate voice mode.

## Conversational Chat

The AI Controller can now have natural conversations! Try these:

### Small Talk
- "Hello" / "Hi" → "Hello! I'm your AI assistant. How can I help you today?"
- "How are you?" → "I'm doing great, thanks for asking! How can I help you today?"
- "Thanks" / "Thank you" → "You're welcome! Anything else I can help with?"
- "Bye" / "Goodbye" → "Goodbye! Have a great day!"
- "What can you do?" → Shows available commands

### Follow-up Questions
- After any command, the AI will ask "Anything else I can help with?"
- "Do it again" → Repeats the last command
- "Yes" / "No" → Conversational responses

## Natural Language Examples

You can now use conversational English! Here are examples:

### System Questions
- "What time is it?" → Current time
- "How is my CPU?" → CPU usage
- "How is my computer doing?" → Full system info
- "What is the date today?" → Current date
- "Can you check my memory?" → Memory usage

### File Operations
- "Create a file called test.txt" → Creates file
- "Read the README.md file" → Shows file contents
- "What files are in the data folder?" → Lists files
- "Search for files with 'config'" → Finds files

### IPO System
- "Run the IPO check" → Runs IPO check
- "Check stock 02408" → Gets stock price
- "Show me the IPO history" → Shows history

### Web & Info
- "Tell me a joke" → Random joke
- "What's an interesting fact?" → Random fact
- "Search for Tesla stock" → Web search
- "What's the weather in Hong Kong?" → Weather info
- "Calculate 2+2*10" → Math result

### Notes
- "Note this is important" → Saves note
- "Read my notes" → Shows notes

## Cloud Deployment (Railway.app)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/hkex-ipo-tracker.git
git push -u origin main
```

### 2. Deploy to Railway
1. Go to: https://railway.app
2. Create new project from GitHub
3. Set environment variables in Railway dashboard
4. Deploy!

## Sample Output

```
* HKEX DAILY REPORT *

Stock: 02408 (XIAO NOODLES)
Date: 07/07/2026 18:05
Type: [Announcement Type]

BUSINESS OVERVIEW:
[Company description and details]

KEY METRICS:
• Market Cap: HKD X.XM
• Revenue: HKD X.XM
• P/E Ratio: X.X
• Sector: [Sector]
• Industry: [Industry]

INVESTMENT ADVANTAGES:
1. Listed on HKEX
2. Operating in [Sector] sector
3. Market cap provides stability
4. Share issuance indicates growth plans

GROWTH ESTIMATES:
[Detailed growth analysis]

RISK FACTORS:
• Market volatility
• Regulatory changes
• Economic conditions

LATEST NEWS:
• [News headline 1]
• [News headline 2]
• [News headline 3]

DOCUMENT: https://www1.hkexnews.hk[link]
```

## Files Structure

```
project001/
├── app.py              # Main entry point for cloud
├── run_ai_controller.py # AI Controller entry point
├── Procfile            # Railway deployment config
├── runtime.txt         # Python version
├── config/
│   ├── config.py       # Configuration settings
│   └── .env           # Your credentials
├── data/
│   ├── ipo_history.json
│   └── ipo_tracker.log
├── src/
│   ├── hkex_detailed.py   # HKEX scraper
│   ├── news_scraper.py    # News scraping
│   ├── discord_sender.py  # Discord integration
│   ├── history_tracker.py
│   ├── ai_summarizer.py
│   └── ai_controller.py   # AI Controller
├── scheduler.py
├── requirements.txt
└── README.md
```

## License

MIT License - Free for personal and commercial use