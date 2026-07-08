"""
HKEX Detailed Scraper
Fetches detailed company information from HKEX announcements
"""
import requests
import logging
from typing import List, Dict, Optional
import yfinance as yf

logger = logging.getLogger(__name__)

# HKEX base URLs
HKEX_BASE_URL = "https://www1.hkexnews.hk/ncms/json/eds"


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
        # HK stocks use .HK suffix
        ticker = yf.Ticker(f"{stock_code}.HK")
        info = ticker.info
        
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
            "website": info.get("website", "N/A"),
            "currency": "HKD"
        }
    except Exception as e:
        logger.error(f"Error fetching stock info for {stock_code}: {e}")
        return None


def generate_detailed_report(announcement: Dict) -> str:
    """Generate a detailed ~1000 word report for an announcement"""
    stock_info = announcement.get("stock", [{}])[0]
    stock_code = stock_info.get("sc", "N/A")
    stock_name = stock_info.get("sn", "N/A")
    title = announcement.get("title", "N/A")
    rel_time = announcement.get("relTime", "N/A")
    web_path = announcement.get("webPath", "N/A")
    
    # Get company details
    company_details = get_hk_stock_info(stock_code)
    
    report = f"* HKEX DAILY REPORT *\n\n"
    report += f"Stock: {stock_code} ({stock_name})\n"
    report += f"Date: {rel_time}\n"
    report += f"Type: {title}\n\n"
    
    if company_details and company_details.get("name") != "N/A":
        # Business Overview (200 words)
        report += "BUSINESS OVERVIEW:\n"
        desc = company_details.get("description", "No description available")
        if len(desc) > 500:
            desc = desc[:500] + "..."
        report += f"{desc}\n\n"
        
        # Key Metrics
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
        
        # Investment Advantages
        report += "INVESTMENT ADVANTAGES:\n"
        report += f"1. Listed on HKEX with stock code {stock_code}\n"
        report += f"2. Operating in {company_details.get('sector', 'N/A')} sector\n"
        report += f"3. Market capitalization of HKD {market_cap/1e6:.1f}M provides stability\n"
        report += f"4. Share issuance indicates potential growth plans\n\n"
        
        # Growth Estimates
        report += "GROWTH ESTIMATES:\n"
        report += f"The {company_details.get('sector', 'N/A')} sector in Hong Kong is expected to show moderate growth.\n"
        report += f"With the company's current revenue of HKD {revenue/1e6:.1f}M, investors should monitor\n"
        report += f"upcoming announcements for specific growth projections. The share issuance program\n"
        report += f"suggests management confidence in future opportunities.\n\n"
        
        # Risk Factors
        report += "RISK FACTORS:\n"
        report += "• Market volatility in Hong Kong stocks\n"
        report += "• Regulatory changes in share issuance\n"
        report += "• Economic conditions affecting the sector\n"
        report += "• Liquidity considerations for smaller companies\n\n"
        
        # Document Link
        report += f"DOCUMENT: https://www1.hkexnews.hk{web_path}\n"
    else:
        # Enhanced report without yfinance data
        report += "BUSINESS OVERVIEW:\n"
        report += f"{stock_name} is a Hong Kong-listed company (Stock Code: {stock_code}) that has recently\n"
        report += "announced a share-related transaction. This indicates potential corporate actions\n"
        report += "that may affect shareholder value.\n\n"
        
        report += "KEY METRICS:\n"
        report += f"• Stock Code: {stock_code}\n"
        report += f"• Company Name: {stock_name}\n"
        report += f"• Announcement Type: {title}\n\n"
        
        report += "INVESTMENT ADVANTAGES:\n"
        report += f"1. Listed on the Hong Kong Stock Exchange (SEHK)\n"
        report += f"2. Active in share management activities\n"
        report += f"3. Transparent regulatory disclosure\n"
        report += f"4. Potential for capital restructuring\n\n"
        
        report += "GROWTH ESTIMATES:\n"
        report += f"Hong Kong-listed companies typically benefit from the region's strong\n"
        report += f"financial infrastructure and access to Asian markets. The share issuance\n"
        report += f"or buyback program suggests management is actively managing capital structure.\n\n"
        
        report += "RISK FACTORS:\n"
        report += "• Market volatility in Hong Kong stocks\n"
        report += "• Regulatory changes in share issuance\n"
        report += "• Economic conditions affecting the sector\n"
        report += "• Liquidity considerations for smaller companies\n\n"
        
        report += f"DOCUMENT: https://www1.hkexnews.hk{web_path}\n"
    
    return report


if __name__ == "__main__":
    # Test the scraper
    announcements = fetch_hkex_announcements()
    print(f"Total announcements: {len(announcements)}")
    
    filtered = filter_ipo_related(announcements)
    print(f"IPO-related announcements: {len(filtered)}")
    
    for ann in filtered[:2]:
        print("\n" + "=" * 50)
        report = generate_detailed_report(ann)
        # Clean for Windows compatibility
        report_clean = report.encode('ascii', 'ignore').decode('ascii')
        print(report_clean)