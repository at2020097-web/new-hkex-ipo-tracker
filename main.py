"""
Main IPO Tracker Script
Orchestrates IPO data collection, summarization, and notification
"""
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ipo_scraper import IPOScraper
from src.ai_summarizer import AISummarizer
from src.whatsapp_sender import WhatsAppSender
from src.history_tracker import HistoryTracker
from config.config import LOG_FILE, CHECK_INTERVAL_MINUTES

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def process_new_ipos():
    """Main function to process and notify about new IPOs"""
    logger.info("Starting IPO check cycle...")
    
    # Initialize components
    scraper = IPOScraper()
    summarizer = AISummarizer()
    sender = WhatsAppSender()
    tracker = HistoryTracker()
    
    # Get all IPOs
    all_ipos = scraper.get_all_ipos()
    logger.info(f"Found {len(all_ipos)} total IPOs")
    
    # Filter to new IPOs only
    new_ipos = tracker.get_new_ipos(all_ipos)
    logger.info(f"Found {len(new_ipos)} new IPOs")
    
    if not new_ipos:
        logger.info("No new IPOs to process")
        return
    
    # Process each new IPO
    for ipo in new_ipos:
        try:
            symbol = ipo.get("symbol", ipo.get("ticker", "N/A"))
            logger.info(f"Processing IPO: {symbol}")
            
            # Get company details
            company_details = scraper.get_company_details(symbol)
            
            # Generate summary
            summary = summarizer.generate_summary(ipo, company_details)
            
            # Send notification
            if sender.is_configured():
                sender.send_ipo_alert(summary)
                logger.info(f"Notification sent for {symbol}")
            else:
                logger.warning(f"WhatsApp not configured. Summary for {symbol}:")
                print(f"\n{summary}\n")
            
            # Add to history
            tracker.add_ipo(ipo)
            
        except Exception as e:
            logger.error(f"Error processing IPO {ipo.get('symbol', 'unknown')}: {e}")
    
    # Cleanup old entries
    tracker.cleanup_old_entries(days=30)
    
    logger.info("IPO check cycle completed")


if __name__ == "__main__":
    process_new_ipos()