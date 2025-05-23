"""
Configuration module for the Sermon Emailer application.
Handles loading and validation of environment variables.
"""

import os
import logging
from typing import List

logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        """Initialize configuration from environment variables."""
        # YouTube API Configuration
        self.youtube_api_key = self._get_required_env('YOUTUBE_API_KEY')
        self.youtube_channel_ids = self._get_channel_ids()
        
        # Email Configuration
        self.sendgrid_api_key = self._get_required_env('SENDGRID_API_KEY')
        self.sender_email = self._get_required_env('SENDER_EMAIL')
        self.recipient_email = self._get_required_env('RECIPIENT_EMAIL')
        
        # Application Settings
        self.check_interval_hours = int(os.getenv('CHECK_INTERVAL_HOURS', '24'))
        
        # Logging Configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE', 'logs/sermon_emailer.log')

    def _get_required_env(self, key: str) -> str:
        """Get a required environment variable or raise an error."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value

    def _get_channel_ids(self) -> List[str]:
        """Get and validate YouTube channel IDs from environment."""
        channel_ids_str = self._get_required_env('YOUTUBE_CHANNEL_IDS')
        channel_ids = [cid.strip() for cid in channel_ids_str.split(',')]
        
        if not channel_ids:
            raise ValueError("No YouTube channel IDs provided")
            
        # Validate channel ID format (should start with UC and be 24 characters)
        for cid in channel_ids:
            if not (cid.startswith('UC') and len(cid) == 24):
                logger.warning(f"Channel ID {cid} may not be in the correct format")
        
        return channel_ids

    def validate(self) -> bool:
        """Validate the configuration."""
        try:
            # Check if all required fields are set
            assert self.youtube_api_key, "YouTube API key is required"
            assert self.youtube_channel_ids, "At least one YouTube channel ID is required"
            assert self.sendgrid_api_key, "SendGrid API key is required"
            assert self.sender_email, "Sender email is required"
            assert self.recipient_email, "Recipient email is required"
            
            # Validate email formats
            assert '@' in self.sender_email, "Invalid sender email format"
            assert '@' in self.recipient_email, "Invalid recipient email format"
            
            # Validate check interval
            assert self.check_interval_hours > 0, "Check interval must be positive"
            
            return True
            
        except AssertionError as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            return False 