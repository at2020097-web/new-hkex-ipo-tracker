"""
Configuration for IPO Tracking System
Replace placeholder values with your actual API keys
"""
import os
from dotenv import load_dotenv

# Load .env from config directory (works in both local and cloud)
config_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(config_dir, '.env')
load_dotenv(env_path)

# API Keys - Get these from respective providers
FINANCIAL_MODELING_PREP_API_KEY = os.getenv("FMP_API_KEY", "YOUR_FMP_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("AV_API_KEY", "YOUR_ALPHA_VANTAGE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

# Twilio Configuration (EASIER FOR TESTING - Free trial available)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "YOUR_TWILIO_WHATSAPP_NUMBER")

# WhatsApp Business API Configuration (Alternative)
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "YOUR_WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "YOUR_PHONE_NUMBER_ID")
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "YOUR_BUSINESS_ACCOUNT_ID")

# Recipient phone numbers (international format, e.g., +1234567890)
RECIPIENT_NUMBERS = os.getenv("RECIPIENT_NUMBERS", "").split(",")  # Comma-separated

# Discord Bot Configuration
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID", "YOUR_DISCORD_CHANNEL_ID")

# Markets to track
MARKETS = ["US", "HK", "UK", "SG", "JP"]  # US, Hong Kong, UK, Singapore, Japan

# Check interval in minutes
CHECK_INTERVAL_MINUTES = 15

# Data storage
IPO_HISTORY_FILE = "data/ipo_history.json"
LOG_FILE = "data/ipo_tracker.log"