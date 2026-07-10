"""
History Tracker Module
Tracks processed IPOs to avoid duplicate notifications
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import json
import logging
from datetime import datetime
from typing import List, Dict, Optional

from config.config import IPO_HISTORY_FILE

logger = logging.getLogger(__name__)


class HistoryTracker:
    def __init__(self, history_file: str = IPO_HISTORY_FILE):
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """Load IPO history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading history: {e}")
        return []
    
    def _save_history(self):
        """Save IPO history to file"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving history: {e}")
    
    def is_processed(self, symbol: str) -> bool:
        """Check if an IPO has already been processed"""
        for entry in self.history:
            if entry.get("symbol") == symbol:
                return True
        return False
    
    def add_ipo(self, ipo_data: Dict):
        """Add a new IPO to history"""
        entry = {
            "symbol": ipo_data.get("symbol", ipo_data.get("ticker", "N/A")),
            "name": ipo_data.get("company", ipo_data.get("name", "N/A")),
            "date_added": datetime.now().isoformat(),
            "expected_date": ipo_data.get("expectedDate", ipo_data.get("date", "N/A"))
        }
        
        # Check if already exists
        if not self.is_processed(entry["symbol"]):
            self.history.append(entry)
            self._save_history()
            logger.info(f"Added {entry['symbol']} to history")
    
    def get_new_ipos(self, ipo_list: List[Dict]) -> List[Dict]:
        """Filter out already processed IPOs"""
        new_ipos = []
        for ipo in ipo_list:
            symbol = ipo.get("symbol", ipo.get("ticker", "N/A"))
            if not self.is_processed(symbol):
                new_ipos.append(ipo)
        return new_ipos
    
    def cleanup_old_entries(self, days: int = 30):
        """Remove old entries from history (older than specified days)"""
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        self.history = [
            entry for entry in self.history
            if datetime.fromisoformat(entry.get("date_added", "2000-01-01")).timestamp() > cutoff
        ]
        self._save_history()


if __name__ == "__main__":
    tracker = HistoryTracker()
    
    # Test
    test_ipo = {"symbol": "TEST", "company": "Test Corp", "expectedDate": "2026-07-15"}
    
    print(f"Is processed: {tracker.is_processed('TEST')}")
    tracker.add_ipo(test_ipo)
    print(f"Is processed after add: {tracker.is_processed('TEST')}")