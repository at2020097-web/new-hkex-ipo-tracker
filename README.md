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
│   └── ai_summarizer.py
├── scheduler.py
├── requirements.txt
└── README.md
```

## License

MIT License - Free for personal and commercial use