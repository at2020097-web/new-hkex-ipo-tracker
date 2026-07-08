"""
WhatsApp Sender Module
Supports both Twilio (for testing) and WhatsApp Business API
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
import logging
from typing import List, Optional
from twilio.rest import Client

from config.config import (
    WHATSAPP_ACCESS_TOKEN,
    WHATSAPP_PHONE_NUMBER_ID,
    RECIPIENT_NUMBERS,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_NUMBER
)

logger = logging.getLogger(__name__)


class WhatsAppSender:
    def __init__(self):
        self.use_twilio = False
        
        # Try Twilio first (easier for testing)
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_WHATSAPP_NUMBER:
            self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            self.from_number = TWILIO_WHATSAPP_NUMBER
            self.use_twilio = True
            logger.info("Using Twilio for WhatsApp")
        else:
            # Fall back to WhatsApp Business API
            self.access_token = WHATSAPP_ACCESS_TOKEN
            self.phone_number_id = WHATSAPP_PHONE_NUMBER_ID
            self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
            logger.info("Using WhatsApp Business API")
    
    def is_configured(self) -> bool:
        """Check if WhatsApp is properly configured"""
        if self.use_twilio:
            return (
                TWILIO_ACCOUNT_SID and 
                TWILIO_ACCOUNT_SID != "YOUR_TWILIO_ACCOUNT_SID" and
                TWILIO_AUTH_TOKEN and
                TWILIO_AUTH_TOKEN != "YOUR_TWILIO_AUTH_TOKEN" and
                TWILIO_WHATSAPP_NUMBER and
                len(RECIPIENT_NUMBERS) > 0
            )
        else:
            return (
                self.access_token and 
                self.access_token != "YOUR_WHATSAPP_ACCESS_TOKEN" and
                self.phone_number_id and
                self.phone_number_id != "YOUR_PHONE_NUMBER_ID" and
                len(RECIPIENT_NUMBERS) > 0
            )
    
    def send_message(self, message: str, recipient: Optional[str] = None) -> bool:
        """Send a message via WhatsApp (handles long messages by splitting)"""
        if not self.is_configured():
            logger.warning("WhatsApp not configured. Message would be: " + message[:100])
            print(f"\n[TEST MODE - No WhatsApp configured]\n{message[:500]}...\n")
            return False
        
        recipients = [recipient] if recipient else RECIPIENT_NUMBERS
        
        # Split long messages (WhatsApp limit is ~4096 characters)
        max_length = 3000
        messages = []
        if len(message) > max_length:
            # Split by lines to preserve formatting
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
        
        for phone in recipients:
            if not phone or phone == "":
                continue
            
            for i, msg in enumerate(messages):
                try:
                    if self.use_twilio:
                        # Twilio format: whatsapp:+1234567890
                        to_number = f"whatsapp:{phone}" if not phone.startswith("whatsapp:") else phone
                        from_number = f"whatsapp:{self.from_number}" if not self.from_number.startswith("whatsapp:") else self.from_number
                        
                        self.client.messages.create(
                            body=msg,
                            from_=from_number,
                            to=to_number
                        )
                        logger.info(f"Message {i+1}/{len(messages)} sent to {phone} via Twilio")
                    else:
                        # WhatsApp Business API
                        headers = {
                            "Authorization": f"Bearer {self.access_token}",
                            "Content-Type": "application/json"
                        }
                        
                        payload = {
                            "messaging_product": "whatsapp",
                            "to": phone,
                            "type": "text",
                            "text": {
                                "body": msg
                            }
                        }
                        
                        response = requests.post(
                            self.base_url,
                            headers=headers,
                            json=payload,
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            logger.info(f"Message {i+1}/{len(messages)} sent to {phone}")
                        else:
                            logger.error(f"Failed to send message to {phone}: {response.text}")
                            
                except Exception as e:
                    logger.error(f"Error sending WhatsApp message: {e}")
        
        return True
    
    def send_ipo_alert(self, ipo_summary: str, recipient: Optional[str] = None) -> bool:
        """Send IPO alert with formatted message"""
        formatted_message = f"🚀 *IPO NOTIFICATION*\n\n{ipo_summary}"
        return self.send_message(formatted_message, recipient)


def send_whatsapp_message(message: str, recipient: Optional[str] = None) -> bool:
    """Convenience function to send WhatsApp message"""
    sender = WhatsAppSender()
    return sender.send_message(message, recipient)


if __name__ == "__main__":
    # Test the sender
    sender = WhatsAppSender()
    
    test_message = """
📈 NEW IPO ALERT

Company: Test Corp (TEST)
Sector: Technology
Price Range: $25-28
Expected Date: 2026-07-15

• Industry: Software - Technology sector
• Market Cap: $1.0B
• Revenue: $100.0M
• Risk Factors: Market volatility, sector-specific risks
• Broker Notes: Review prospectus before investing
    """
    
    print("Testing WhatsApp sender...")
    print(f"Configured: {sender.is_configured()}")
    print(f"Using Twilio: {sender.use_twilio}")
    sender.send_message(test_message)