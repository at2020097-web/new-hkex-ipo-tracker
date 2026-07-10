"""
Discord Bot Sender Module
Sends IPO reports to Discord channel
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
import logging
from typing import Optional

from config.config import DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID

logger = logging.getLogger(__name__)


class DiscordSender:
    def __init__(self):
        self.bot_token = DISCORD_BOT_TOKEN
        self.channel_id = DISCORD_CHANNEL_ID
        self.base_url = f"https://discord.com/api/v10/channels/{self.channel_id}/messages"
    
    def is_configured(self) -> bool:
        """Check if Discord is properly configured"""
        return (
            self.bot_token and 
            self.bot_token != "YOUR_DISCORD_BOT_TOKEN" and
            self.channel_id and
            self.channel_id != "YOUR_DISCORD_CHANNEL_ID"
        )
    
    def send_message(self, message: str) -> bool:
        """Send a message to Discord channel (handles long messages)"""
        if not self.is_configured():
            logger.warning("Discord not configured. Message would be: " + message[:100])
            print(f"\n[TEST MODE - No Discord configured]\n{message[:500]}...\n")
            return False
        
        # Split long messages (Discord limit is 2000 characters)
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
                    "Authorization": f"Bot {self.bot_token}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "content": msg
                }
                
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    logger.info(f"Message {i+1}/{len(messages)} sent to Discord")
                    print(f"Message {i+1}/{len(messages)} sent successfully")
                else:
                    logger.error(f"Failed to send message to Discord: {response.status_code} - {response.text}")
                    print(f"Failed to send: {response.status_code} - {response.text}")
                    
            except Exception as e:
                logger.error(f"Error sending Discord message: {e}")
                print(f"Error: {e}")
        
        return True


def send_discord_message(message: str) -> bool:
    """Convenience function to send Discord message"""
    sender = DiscordSender()
    return sender.send_message(message)


if __name__ == "__main__":
    sender = DiscordSender()
    
    test_message = """
* HKEX DAILY REPORT *

Stock: 02408 (TEST COMPANY)
Date: 07/07/2026 18:05

BUSINESS OVERVIEW:
This is a test company for demonstration purposes.

KEY METRICS:
• Market Cap: HKD 100.0M
• Revenue: HKD 50.0M
• P/E Ratio: 10.5

INVESTMENT ADVANTAGES:
1. Listed on HKEX
2. Strong market position
3. Growth potential

GROWTH ESTIMATES:
The sector is expected to grow moderately.

RISK FACTORS:
• Market volatility
• Regulatory changes
    """
    
    print("Testing Discord sender...")
    print(f"Configured: {sender.is_configured()}")
    sender.send_message(test_message)