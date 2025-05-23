"""
Email service module for sending sermon emails using SendGrid.
"""

import logging
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, api_key: str, sender_email: str, recipient_email: str):
        """
        Initialize email service with SendGrid credentials.
        
        Args:
            api_key: SendGrid API key
            sender_email: Verified sender email address
            recipient_email: Recipient email address
        """
        self.sg = SendGridAPIClient(api_key)
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        
    def send_email(self, subject: str, body: str) -> bool:
        """
        Send an email using SendGrid.
        
        Args:
            subject: Email subject
            body: Email body (plain text)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            message = Mail(
                from_email=Email(self.sender_email),
                to_emails=To(self.recipient_email),
                subject=subject,
                plain_text_content=Content("text/plain", body)
            )
            
            response = self.sg.send(message)
            
            if response.status_code == 202:
                logger.info(f"Email sent successfully to {self.recipient_email}")
                return True
            else:
                logger.error(f"Failed to send email. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
            
    def send_html_email(self, subject: str, html_body: str, plain_text_body: Optional[str] = None) -> bool:
        """
        Send an HTML email using SendGrid.
        
        Args:
            subject: Email subject
            html_body: Email body in HTML format
            plain_text_body: Optional plain text version of the email
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            message = Mail(
                from_email=Email(self.sender_email),
                to_emails=To(self.recipient_email),
                subject=subject
            )
            
            # Add HTML content
            message.content = Content("text/html", html_body)
            
            # Add plain text content if provided
            if plain_text_body:
                message.content = Content("text/plain", plain_text_body)
            
            response = self.sg.send(message)
            
            if response.status_code == 202:
                logger.info(f"HTML email sent successfully to {self.recipient_email}")
                return True
            else:
                logger.error(f"Failed to send HTML email. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending HTML email: {str(e)}")
            return False 