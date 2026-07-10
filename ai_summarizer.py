"""
AI Summarization Module
Generates detailed IPO summaries with industry analysis
All currencies expressed in HKD
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import openai
import logging
from typing import Dict, Optional
import json

from config.config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

# Use OpenAI or fallback to rule-based summarization
USE_OPENAI = OPENAI_API_KEY and OPENAI_API_KEY != "YOUR_OPENAI_API_KEY"

# HKD conversion rate (approximate, can be updated dynamically)
USD_TO_HKD_RATE = 7.8  # 1 USD = 7.8 HKD (approximate)


def usd_to_hkd(amount_usd: float) -> float:
    """Convert USD to HKD"""
    return amount_usd * USD_TO_HKD_RATE


def format_currency_hkd(amount: float) -> str:
    """Format currency in HKD with appropriate units (input is in USD)"""
    hkd_amount = amount * USD_TO_HKD_RATE  # Convert USD to HKD
    if hkd_amount >= 1e9:
        return f"HKD {hkd_amount/1e9:.2f}B"
    elif hkd_amount >= 1e6:
        return f"HKD {hkd_amount/1e6:.1f}M"
    elif hkd_amount >= 1e3:
        return f"HKD {hkd_amount/1e3:.1f}K"
    else:
        return f"HKD {hkd_amount:.0f}"


class AISummarizer:
    def __init__(self):
        if USE_OPENAI:
            openai.api_key = OPENAI_API_KEY
    
    def generate_summary(self, ipo_data: Dict, company_details: Optional[Dict] = None) -> str:
        """Generate a comprehensive IPO summary with bullet points"""
        
        if USE_OPENAI and company_details:
            return self._generate_ai_summary(ipo_data, company_details)
        else:
            return self._generate_rule_based_summary(ipo_data, company_details)
    
    def _generate_ai_summary(self, ipo_data: Dict, company_details: Optional[Dict] = None) -> str:
        """Use OpenAI to generate detailed summary"""
        try:
            prompt = f"""
            Generate a comprehensive IPO analysis summary for investors and brokers.
            
            IPO Data:
            {json.dumps(ipo_data, indent=2)}
            
            Company Details:
            {json.dumps(company_details, indent=2) if company_details else "Not available"}
            
            Include:
            1. Industry overview and market position
            2. Key financial metrics and growth indicators (express in HKD)
            3. Competitive landscape and major competitors
            4. Risk factors for investors
            5. Broker/investor considerations
            
            Format as bullet points, keep it concise but informative.
            All currency values should be expressed in HKD.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst providing IPO analysis for professional investors and brokers. Express all currency values in HKD (Hong Kong Dollars)."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message['content']
        except Exception as e:
            logger.error(f"Error generating AI summary: {e}")
            return self._generate_rule_based_summary(ipo_data, company_details)
    
    def _generate_rule_based_summary(self, ipo_data: Dict, company_details: Optional[Dict] = None) -> str:
        """Generate summary without AI (fallback method) - All currencies in HKD"""
        symbol = ipo_data.get("symbol", ipo_data.get("ticker", "N/A"))
        name = ipo_data.get("company", ipo_data.get("name", "N/A"))
        
        summary = f"📈 NEW IPO ALERT\n\n"
        summary += f"Company: {name} ({symbol})\n"
        
        if company_details:
            summary += f"Sector: {company_details.get('sector', 'N/A')}\n"
            summary += f"Industry: {company_details.get('industry', 'N/A')}\n"
        
        price_range = ipo_data.get("priceRange", ipo_data.get("price", "N/A"))
        if price_range:
            summary += f"Price Range: {price_range}\n"
        
        expected_date = ipo_data.get("expectedDate", ipo_data.get("date", "N/A"))
        if expected_date:
            summary += f"Expected Date: {expected_date}\n"
        
        summary += "\n"
        
        # Key metrics - converted to HKD
        if company_details:
            market_cap = company_details.get("market_cap", "N/A")
            if market_cap and market_cap != "N/A":
                hkd_value = usd_to_hkd(market_cap)
                summary += f"• Market Cap: {format_currency_hkd(market_cap)}\n"
            
            revenue = company_details.get("revenue", "N/A")
            if revenue and revenue != "N/A":
                summary += f"• Revenue: {format_currency_hkd(revenue)}\n"
            
            employees = company_details.get("employees", "N/A")
            if employees and employees != "N/A":
                summary += f"• Employees: {employees}\n"
        
        # Description
        if company_details and company_details.get("description"):
            desc = company_details.get("description", "")[:200] + "..." if len(company_details.get("description", "")) > 200 else company_details.get("description", "")
            summary += f"• Business: {desc}\n"
        
        # Industry analysis
        if company_details:
            sector = company_details.get("sector", "N/A")
            industry = company_details.get("industry", "N/A")
            summary += f"• Industry: {industry} ({sector})\n"
        
        # Risk factors
        summary += "• Risk Factors: Market volatility, sector-specific risks, new public company\n"
        
        # Broker notes
        summary += "• Broker Notes: Review prospectus before investing, consider lock-up period\n"
        
        return summary
    
    def generate_industry_overview(self, sector: str, industry: str) -> str:
        """Generate industry overview using AI"""
        if USE_OPENAI:
            try:
                prompt = f"""
                Provide a brief industry overview for {industry} sector ({sector}).
                Include:
                - Current market size and growth trends
                - Key drivers and challenges
                - Typical valuation multiples
                - Recent M&A activity
                
                Keep it concise (3-4 bullet points).
                """
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a financial industry analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.5
                )
                
                return response.choices[0].message['content']
            except Exception as e:
                logger.error(f"Error generating industry overview: {e}")
        
        return f"• Industry: {industry} - {sector} sector\n• Monitor sector trends and economic conditions\n"


if __name__ == "__main__":
    summarizer = AISummarizer()
    
    # Test with sample data
    test_ipo = {
        "symbol": "TEST",
        "company": "Test Company",
        "priceRange": "$25-28",
        "expectedDate": "2026-07-15"
    }
    
    test_details = {
        "sector": "Technology",
        "industry": "Software",
        "description": "A software company providing cloud solutions",
        "market_cap": 1000000000,  # $1B USD
        "revenue": 100000000,      # $100M USD
        "employees": 500
    }
    
    print(summarizer.generate_summary(test_ipo, test_details))