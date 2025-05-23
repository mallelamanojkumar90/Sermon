#!/usr/bin/env python3
"""
Daily Telugu Bible Sermon Email Assistant
Main application file that orchestrates the sermon selection and email delivery process.
"""

import os
import logging
import random
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from youtube_service import YouTubeService
from email_service import EmailService
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/sermon_emailer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SermonEmailer:
    def __init__(self):
        """Initialize the SermonEmailer with configuration and services."""
        # Load environment variables
        load_dotenv()
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Initialize configuration
        self.config = Config()
        
        # Initialize services
        self.youtube_service = YouTubeService(self.config.youtube_api_key)
        self.email_service = EmailService(
            self.config.sendgrid_api_key,
            self.config.sender_email,
            self.config.recipient_email
        )
        
        # Track last sermon sent
        self.last_sermon_date = None
        self.last_sermon_id = None

    def get_random_sermon(self):
        """Fetch a random sermon from configured YouTube channels."""
        try:
            # Get videos from all configured channels
            all_videos = []
            for channel_id in self.config.youtube_channel_ids:
                videos = self.youtube_service.get_channel_videos(channel_id)
                all_videos.extend(videos)
            
            if not all_videos:
                logger.error("No sermons found in configured channels")
                return None
            
            # Select a random sermon that hasn't been sent recently
            available_videos = [v for v in all_videos if v['id'] != self.last_sermon_id]
            if not available_videos:
                available_videos = all_videos  # Reset if we've sent all sermons
            
            selected_video = random.choice(available_videos)
            self.last_sermon_id = selected_video['id']
            
            return {
                'title': selected_video['title'],
                'url': f"https://www.youtube.com/watch?v={selected_video['id']}",
                'channel_title': selected_video['channel_title']
            }
            
        except Exception as e:
            logger.error(f"Error fetching random sermon: {str(e)}")
            return None

    def send_daily_sermon(self):
        """Main function to send the daily sermon."""
        try:
            # Check if we've already sent a sermon today
            today = datetime.now().date()
            if self.last_sermon_date == today:
                logger.info("Sermon already sent today")
                return
            
            # Get random sermon
            sermon = self.get_random_sermon()
            if not sermon:
                logger.error("Failed to get sermon")
                return
            
            # Prepare email content
            subject = "మీ రోజువారీ తెలుగు బైబిల్ ప్రసంగం (Your Daily Telugu Bible Sermon)"
            body = f"""
నమస్కారం (Greetings),

ఈ రోజు మీకోసం ఎంచుకోబడిన ప్రసంగం ఇక్కడ ఉంది (Here is the sermon selected for you today):

ప్రసంగం పేరు (Sermon Title): {sermon['title']}
ప్రసంగకర్త (Speaker): {sermon['channel_title']}
వినడానికి/చూడటానికి లింక్ (Link to listen/watch): {sermon['url']}

దేవుడు మిమ్మును దీవించును గాక (May God bless you),
మీ తెలుగు ప్రసంగాల సహాయకుడు (Your Telugu Sermons Assistant)
"""
            
            # Send email
            success = self.email_service.send_email(subject, body)
            
            if success:
                self.last_sermon_date = today
                logger.info(f"Successfully sent sermon: {sermon['title']}")
            else:
                logger.error("Failed to send sermon email")
                
        except Exception as e:
            logger.error(f"Error in send_daily_sermon: {str(e)}")

    def run(self):
        """Run the sermon emailer on schedule."""
        logger.info("Starting Sermon Emailer service")
        
        # Schedule the job
        schedule.every(self.config.check_interval_hours).hours.do(self.send_daily_sermon)
        
        # Run immediately on startup
        self.send_daily_sermon()
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    try:
        sermon_emailer = SermonEmailer()
        sermon_emailer.run()
    except KeyboardInterrupt:
        logger.info("Sermon Emailer service stopped by user")
    except Exception as e:
        logger.error(f"Sermon Emailer service stopped due to error: {str(e)}") 