"""
News Scraper Module
Scrapes financial news from AAStocks, SCMP, and Bloomberg
"""
import requests
import logging
from typing import List, Dict
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def scrape_aastocks_news(stock_code: str) -> List[Dict]:
    """Scrape news from AAStocks for a specific stock"""
    try:
        url = f"https://www.aastocks.com/tc/listed/stock/{stock_code}/news"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = []
        
        # Find news headlines (AAStocks structure)
        for item in soup.find_all('div', class_='newshead')[:5]:
            title = item.get_text(strip=True)
            link = item.find('a')
            if link and link.get('href'):
                news_items.append({
                    "title": title,
                    "url": f"https://www.aastocks.com{link.get('href')}",
                    "source": "AAStocks"
                })
        
        return news_items
    except Exception as e:
        logger.error(f"Error scraping AAStocks for {stock_code}: {e}")
        return []


def scrape_scmp_finance_news() -> List[Dict]:
    """Scrape latest finance news from SCMP"""
    try:
        url = "https://www.scmp.com/business/finance"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = []
        
        # Find article headlines
        for item in soup.find_all('h3', class_='article-title')[:5]:
            title = item.get_text(strip=True)
            link = item.find('a')
            if link and link.get('href'):
                news_items.append({
                    "title": title,
                    "url": f"https://www.scmp.com{link.get('href')}" if link.get('href').startswith('/') else link.get('href'),
                    "source": "SCMP"
                })
        
        return news_items
    except Exception as e:
        logger.error(f"Error scraping SCMP: {e}")
        return []


def scrape_bloomberg_news() -> List[Dict]:
    """Scrape latest finance news from Bloomberg"""
    try:
        url = "https://www.bloomberg.com/markets"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = []
        
        # Find headlines
        for item in soup.find_all('a', class_='headline__3a97474271')[:5]:
            title = item.get_text(strip=True)
            if title:
                news_items.append({
                    "title": title,
                    "url": f"https://www.bloomberg.com{item.get('href')}" if item.get('href') else "",
                    "source": "Bloomberg"
                })
        
        return news_items
    except Exception as e:
        logger.error(f"Error scraping Bloomberg: {e}")
        return []


def get_all_news(stock_code: str = None) -> List[Dict]:
    """Get news from all sources"""
    all_news = []
    
    if stock_code:
        all_news.extend(scrape_aastocks_news(stock_code))
    
    all_news.extend(scrape_scmp_finance_news())
    all_news.extend(scrape_bloomberg_news())
    
    return all_news[:10]  # Limit to 10 news items


if __name__ == "__main__":
    # Test the scraper
    print("Testing news scraper...")
    news = get_all_news("0001")
    for item in news:
        print(f"- {item['source']}: {item['title']}")