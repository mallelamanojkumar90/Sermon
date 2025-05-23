# Daily Telugu Bible Sermon Email Assistant

This Python application automatically sends a random Telugu Bible sermon to your email address every day. It sources sermons from YouTube channels and sends them via email using the SendGrid API.

## Features

- Daily automated sermon delivery
- Random sermon selection from YouTube channels
- Email delivery using SendGrid
- Configurable sermon sources and email settings
- Logging of sermon delivery status

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your configuration (see `.env.example`)
4. Set up YouTube API credentials:
   - Go to Google Cloud Console
   - Create a project
   - Enable YouTube Data API v3
   - Create credentials (API key)
5. Set up SendGrid:
   - Create a SendGrid account
   - Create an API key
   - Verify your sender email address

## Configuration

Create a `.env` file with the following variables:

```
# YouTube API Configuration
YOUTUBE_API_KEY=your_youtube_api_key
YOUTUBE_CHANNEL_IDS=channel_id1,channel_id2

# Email Configuration
SENDGRID_API_KEY=your_sendgrid_api_key
SENDER_EMAIL=your_verified_sender_email
RECIPIENT_EMAIL=your_email@example.com

# Application Settings
CHECK_INTERVAL_HOURS=24
```

## Usage

Run the application:

```bash
python sermon_emailer.py
```

The application will:
1. Check for new sermons daily
2. Randomly select a sermon
3. Send it to your email
4. Log the delivery status

## Logging

Logs are stored in `logs/sermon_emailer.log` and include:
- Sermon selection
- Email delivery status
- Any errors or issues

## Contributing

Feel free to submit issues and enhancement requests!
