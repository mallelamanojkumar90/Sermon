"""
YouTube service module for fetching sermon videos from YouTube channels.
"""

import logging
from typing import List, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self, api_key: str):
        """Initialize YouTube service with API key."""
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get videos from a YouTube channel.
        
        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to fetch (default: 50)
            
        Returns:
            List of video dictionaries containing id, title, and channel_title
        """
        try:
            # First, get the channel's uploads playlist ID
            channel_response = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            if not channel_response['items']:
                logger.error(f"Channel {channel_id} not found")
                return []
                
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from the uploads playlist
            videos = []
            next_page_token = None
            
            while len(videos) < max_results:
                playlist_response = self.youtube.playlistItems().list(
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token
                ).execute()
                
                for item in playlist_response['items']:
                    video = {
                        'id': item['snippet']['resourceId']['videoId'],
                        'title': item['snippet']['title'],
                        'channel_title': item['snippet']['channelTitle'],
                        'published_at': item['snippet']['publishedAt']
                    }
                    videos.append(video)
                
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
            
            logger.info(f"Retrieved {len(videos)} videos from channel {channel_id}")
            return videos
            
        except HttpError as e:
            logger.error(f"YouTube API error: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching videos from channel {channel_id}: {str(e)}")
            return []
            
    def get_video_details(self, video_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary containing video details
        """
        try:
            response = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            ).execute()
            
            if not response['items']:
                logger.error(f"Video {video_id} not found")
                return {}
                
            video = response['items'][0]
            return {
                'id': video['id'],
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'channel_title': video['snippet']['channelTitle'],
                'published_at': video['snippet']['publishedAt'],
                'duration': video['contentDetails']['duration'],
                'view_count': video['statistics']['viewCount'],
                'like_count': video['statistics'].get('likeCount', '0')
            }
            
        except HttpError as e:
            logger.error(f"YouTube API error: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Error fetching video details for {video_id}: {str(e)}")
            return {} 