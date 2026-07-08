"""
IPO Data Collection Module
Gathers IPO information from multiple financial APIs
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import yfinance as yf

from config.config import (
    FINANCIAL_MODELING_PREP_API_KEY,
    ALPHA_VANTAGE_API_KEY,
    MARKETS
)

logger = logging.getLogger(__name__)


class IPOScraper:
    def __init__(self):
        self.fmp_base_url = "https://financialmodelingprep.com/api/v3"
        self.av_base_url = "https://www.alphavantage.co/query"
        
    def get_ipos_fmp(self) -> List[Dict]:
        """Get IPO data from Financial Modeling Prep API"""
        try:
            # Get today's IPOs
            url = f"{self.fmp_base_url}/ipo"
            params = {
                "apikey": FINANCIAL_MODELING_PREP_API_KEY
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Also get upcoming IPOs
            upcoming_url = f"{self.fmp_base_url}/ipo-calendar"
            upcoming_response = requests.get(upcoming_url, params=params, timeout=10)
            upcoming_response.raise_for_status()
            upcoming_data = upcoming_response.json()
            
            return data + upcoming_data
        except Exception as e:
            logger.error(f"Error fetching IPOs from FMP: {e}")
            return []
    
    def get_ipos_yahoo(self) -> List[Dict]:
        """Get IPO data from Yahoo Finance (fallback)"""
        try:
            # Yahoo Finance doesn't have direct IPO endpoint, but we can check new listings
            # This is a simplified approach - in production, you'd use a more robust source
            ipos = []
            
            # Check for recent IPO listings (stocks that went public in last 30 days)
            # This is a placeholder - real implementation would use a proper IPO calendar
            return ipos
        except Exception as e:
            logger.error(f"Error fetching IPOs from Yahoo: {e}")
            return []
    
    def get_company_details(self, symbol: str) -> Optional[Dict]:
        """Get detailed company information using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                "symbol": symbol,
                "name": info.get("longName", info.get("shortName", "N/A")),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "description": info.get("longBusinessSummary", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "revenue": info.get("totalRevenue", "N/A"),
                "employees": info.get("fullTimeEmployees", "N/A"),
                "website": info.get("website", "N/A"),
                "financials": self._get_financials(ticker)
            }
        except Exception as e:
            logger.error(f"Error fetching company details for {symbol}: {e}")
            return None
    
    def _get_financials(self, ticker) -> Dict:
        """Extract key financial metrics"""
        try:
            financials = ticker.financials
            if financials is not None and not financials.empty:
                latest = financials.iloc[:, 0]
                return {
                    "revenue": float(latest.get("Total Revenue", 0)) if latest.get("Total Revenue") else 0,
                    "gross_profit": float(latest.get("Gross Profit", 0)) if latest.get("Gross Profit") else 0,
                    "net_income": float(latest.get("Net Income", 0)) if latest.get("Net Income") else 0,
                }
        except:
            pass
        return {}
    
    def get_industry_peers(self, symbol: str) -> List[str]:
        """Get industry peers/competitors for a company"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            sector = info.get("sector", "")
            
            # This is a simplified version - in production, you'd use a more robust peer lookup
            # For now, return empty list as we'll use AI to identify competitors
            return []
        except Exception as e:
            logger.error(f"Error fetching industry peers for {symbol}: {e}")
            return []
    
    def get_all_ipos(self) -> List[Dict]:
        """Aggregate IPO data from all sources"""
        all_ipos = []
        
        # Get from FMP
        fmp_ipos = self.get_ipos_fmp()
        all_ipos.extend(fmp_ipos)
        
        # Remove duplicates based on symbol
        seen_symbols = set()
        unique_ipos = []
        for ipo in all_ipos:
            symbol = ipo.get("symbol", ipo.get("ticker", ""))
            if symbol and symbol not in seen_symbols:
                seen_symbols.add(symbol)
                unique_ipos.append(ipo)
        
        return unique_ipos


if __name__ == "__main__":
    scraper = IPOScraper()
    ipos = scraper.get_all_ipos()
    print(json.dumps(ipos, indent=2))