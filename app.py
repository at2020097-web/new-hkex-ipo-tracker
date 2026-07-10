"""
HKEX IPO Tracker - Single File for Railway Deployment
All-in-one script that doesn't require complex imports
Runs continuously 24/7
"""
import os
import sys
import json
import time
import requests
import logging
from datetime import datetime
from typing import List, Dict, Optional
import yfinance as yf
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration - Load from environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID", "")
ALPHA_VANTAGE_API_KEY = os.getenv("AV_API_KEY", "")

# HKEX base URLs
HKEX_BASE_URL = "https://www1.hkexnews.hk/ncms/json/eds"

# Data storage
IPO_HISTORY_FILE = "/app/data/ipo_history.json"

# Check interval in minutes
CHECK_INTERVAL = 15


def load_history() -> List[Dict]:
    """Load IPO history from file"""
    if os.path.exists(IPO_HISTORY_FILE):
        try:
            with open(IPO_HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return []


def save_history(history: List[Dict]):
    """Save IPO history to file"""
    try:
        os.makedirs(os.path.dirname(IPO_HISTORY_FILE), exist_ok=True)
        with open(IPO_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving history: {e}")


def is_processed(symbol: str) -> bool:
    """Check if an IPO has already been processed"""
    history = load_history()
    for entry in history:
        if entry.get("symbol") == symbol:
            return True
    return False


def add_to_history(symbol: str, name: str):
    """Add a new IPO to history"""
    history = load_history()
    if not is_processed(symbol):
        history.append({
            "symbol": symbol,
            "name": name,
            "date_added": datetime.now().isoformat()
        })
        save_history(history)


def fetch_hkex_announcements() -> List[Dict]:
    """Fetch all HKEX announcements from both JSON files"""
    all_announcements = []
    
    for i in range(1, 3):
        try:
            url = f"{HKEX_BASE_URL}/lcisehk1relsde_{i}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            announcements = data.get("newsInfoLst", [])
            all_announcements.extend(announcements)
            logger.info(f"Fetched {len(announcements)} announcements from file {i}")
        except Exception as e:
            logger.error(f"Error fetching HKEX file {i}: {e}")
    
    return all_announcements


def filter_ipo_related(announcements: List[Dict]) -> List[Dict]:
    """Filter announcements related to share issuance/IPO"""
    keywords = ["ISSUE SHARE", "NEW SHARE", "SHARE BUYBACK", "REPURCHASE", "GENERAL MANDATE"]
    
    filtered = []
    for ann in announcements:
        title = ann.get("title", "").upper()
        ltxt = ann.get("lTxt", "").upper()
        
        if any(kw in title or kw in ltxt for kw in keywords):
            filtered.append(ann)
    
    return filtered


def get_hk_stock_info(stock_code: str) -> Optional[Dict]:
    """Get detailed stock information using yfinance (HK stocks)"""
    try:
        ticker = yf.Ticker(f"{stock_code}.HK")
        info = ticker.info
        
        # Check if we got valid data
        if not info or info.get("longName") is None:
            return None
        
        return {
            "symbol": f"{stock_code}.HK",
            "name": info.get("longName", info.get("shortName", "N/A")),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "description": info.get("longBusinessSummary", "N/A"),
            "market_cap": info.get("marketCap", 0),
            "revenue": info.get("totalRevenue", 0),
            "employees": info.get("fullTimeEmployees", 0),
            "pe_ratio": info.get("trailingPE", 0),
            "currency": "HKD"
        }
    except Exception as e:
        logger.error(f"Error fetching stock info for {stock_code}: {e}")
        return None


def scrape_news(stock_code: str) -> List[Dict]:
    """Scrape news from AAStocks, SCMP, and Bloomberg"""
    news_items = []
    
    # AAStocks news
    try:
        url = f"https://www.aastocks.com/tc/listed/stock/{stock_code}/news"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.find_all('div', class_='newshead')[:2]:
                title = item.get_text(strip=True)
                if title:
                    news_items.append({"title": title, "source": "AAStocks"})
    except:
        pass
    
    # SCMP Finance news
    try:
        url = "https://www.scmp.com/business/finance"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.find_all('h3', class_='article-title')[:2]:
                title = item.get_text(strip=True)
                if title:
                    news_items.append({"title": title, "source": "SCMP"})
    except:
        pass
    
    return news_items[:3]


def generate_detailed_report(announcement: Dict) -> str:
    """Generate a detailed ~1000 word report for an announcement"""
    stock_info = announcement.get("stock", [{}])[0]
    stock_code = stock_info.get("sc", "N/A")
    stock_name = stock_info.get("sn", "N/A")
    title = announcement.get("title", "N/A")
    rel_time = announcement.get("relTime", "N/A")
    web_path = announcement.get("webPath", "N/A")
    
    company_details = get_hk_stock_info(stock_code)
    
    report = f"* HKEX DAILY REPORT *\n\n"
    report += f"Stock: {stock_code} ({stock_name})\n"
    report += f"Date: {rel_time}\n"
    report += f"Type: {title}\n\n"
    
    if company_details and company_details.get("name") != "N/A":
        report += "BUSINESS OVERVIEW:\n"
        desc = company_details.get("description", "No description available")
        if len(desc) > 500:
            desc = desc[:500] + "..."
        report += f"{desc}\n\n"
        
        report += "KEY METRICS:\n"
        market_cap = company_details.get("market_cap", 0)
        if market_cap:
            report += f"• Market Cap: HKD {market_cap/1e6:.1f}M\n"
        revenue = company_details.get("revenue", 0)
        if revenue:
            report += f"• Revenue: HKD {revenue/1e6:.1f}M\n"
        pe = company_details.get("pe_ratio", 0)
        if pe:
            report += f"• P/E Ratio: {pe:.2f}\n"
        employees = company_details.get("employees", 0)
        if employees:
            report += f"• Employees: {employees}\n"
        report += f"• Sector: {company_details.get('sector', 'N/A')}\n"
        report += f"• Industry: {company_details.get('industry', 'N/A')}\n\n"
        
        report += "INVESTMENT ADVANTAGES:\n"
        report += f"1. Listed on HKEX with stock code {stock_code}\n"
        report += f"2. Operating in {company_details.get('sector', 'N/A')} sector\n"
        report += f"3. Market cap provides stability\n"
        report += f"4. Share issuance indicates growth plans\n\n"
        
        report += "GROWTH ESTIMATES:\n"
        report += f"The {company_details.get('sector', 'N/A')} sector in Hong Kong shows moderate growth.\n"
        report += f"With revenue of HKD {revenue/1e6:.1f}M, investors should monitor announcements.\n\n"
        
        report += "RISK FACTORS:\n"
        report += "• Market volatility in Hong Kong stocks\n"
        report += "• Regulatory changes in share issuance\n"
        report += "• Economic conditions affecting the sector\n\n"
        
        report += f"DOCUMENT: https://www1.hkexnews.hk{web_path}\n"
    else:
        report += "BUSINESS OVERVIEW:\n"
        report += f"{stock_name} is a Hong Kong-listed company (Stock Code: {stock_code}) that has recently\n"
        report += "announced a share-related transaction.\n\n"
        
        report += "KEY METRICS:\n"
        report += f"• Stock Code: {stock_code}\n"
        report += f"• Company Name: {stock_name}\n\n"
        
        report += "INVESTMENT ADVANTAGES:\n"
        report += f"1. Listed on the Hong Kong Stock Exchange\n"
        report += f"2. Active in share management activities\n\n"
        
        report += "GROWTH ESTIMATES:\n"
        report += f"Hong Kong-listed companies benefit from the region's strong financial infrastructure.\n\n"
        
        report += "RISK FACTORS:\n"
        report += "• Market volatility\n"
        report += "• Regulatory changes\n\n"
        
        report += f"DOCUMENT: https://www1.hkexnews.hk{web_path}\n"
    
    # Add news clippings
    news = scrape_news(stock_code)
    if news:
        report += "\nLATEST NEWS CLIPPINGS:\n"
        for n in news:
            report += f"• [{n['source']}] {n['title']}\n"
    
    return report


def send_discord_message(message: str) -> bool:
    """Send a message to Discord channel"""
    if not DISCORD_BOT_TOKEN or not DISCORD_CHANNEL_ID:
        print(f"\n[TEST MODE - No Discord configured]\n{message[:500]}...\n")
        return False
    
    max_length = 1900
    messages = []
    if len(message) > max_length:
        lines = message.split('\n')
        current_msg = ""
        for line in lines:
            if len(current_msg + line) > max_length:
                messages.append(current_msg)
                current_msg = line + "\n"
            else:
                current_msg += line + "\n"
        if current_msg:
            messages.append(current_msg)
    else:
        messages = [message]
    
    for i, msg in enumerate(messages):
        try:
            headers = {
                "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
                "Content-Type": "application/json"
            }
            
            payload = {"content": msg}
            
            response = requests.post(
                f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}/messages",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"Message {i+1}/{len(messages)} sent successfully")
            else:
                print(f"Failed to send: {response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    return True


def run_hkex_reports():
    """Run HKEX reports and send to Discord"""
    print("Fetching HKEX announcements...")
    
    announcements = fetch_hkex_announcements()
    print(f"Total announcements: {len(announcements)}")
    
    filtered = filter_ipo_related(announcements)
    print(f"IPO-related announcements: {len(filtered)}")
    
    for ann in filtered[:5]:
        stock_info = ann.get("stock", [{}])[0]
        stock_code = stock_info.get("sc", "N/A")
        
        if is_processed(stock_code):
            print(f"Skipping {stock_code} - already processed")
            continue
        
        print(f"Processing {stock_code}...")
        
        report = generate_detailed_report(ann)
        send_discord_message(report)
        add_to_history(stock_code, stock_info.get("sn", "N/A"))


def main():
    """Main loop - runs continuously"""
    print("Starting HKEX IPO Tracker - Running 24/7")
    print(f"Check interval: {CHECK_INTERVAL} minutes")
    
    while True:
        try:
            run_hkex_reports()
            print(f"\nSleeping for {CHECK_INTERVAL} minutes...")
            time.sleep(CHECK_INTERVAL * 60)
        except KeyboardInterrupt:
            print("Stopping...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait 1 minute before retry


if __name__ == "__main__":
    main()