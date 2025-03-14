import os
import pickle
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"

# If modifying the OAuth scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']  # Scopes depending on your needs

class YouTubeAPI:
    def __init__(self):
        self.youtube = None
        self.credentials = None

        # Check if we have saved credentials (token.pickle)
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)
        
        # If no credentials, ask for login via OAuth
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                self.authenticate()

        # Build the YouTube API client
        self.youtube = build('youtube', 'v3', credentials=self.credentials)

    def authenticate(self):
        """Authenticate and save credentials for future use."""
        try:
            # Adjust the path to point to the correct location of client_secrets.json
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json'), SCOPES)
        except FileNotFoundError:
            print(f"{RED}ERROR: client_secrets.json not found!{RESET}")
            print(f"{YELLOW}Please follow the setup instructions in README.md to create your credentials.{RESET}")
            exit(1)
            
        self.credentials = flow.run_local_server(port=0)  # This will open a web browser for login
        # Save credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(self.credentials, token)


    def get_live_status(self, channel_id):
        """Check if a channel is currently live and get upcoming streams."""
        # Get uploads playlist ID
        channels_response = self.youtube.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()
        
        if not channels_response['items']:
            return {"live": False, "upcoming": []}
        
        uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Get recent videos
        videos_response = self.youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=10
        ).execute()
        
        video_ids = [item['snippet']['resourceId']['videoId'] for item in videos_response['items']]
        
        # Get video details including live status
        if video_ids:
            videos_details = self.youtube.videos().list(
                part="snippet,contentDetails,status,liveStreamingDetails",
                id=",".join(video_ids)
            ).execute()
            
            live_streams = []
            upcoming_streams = []
            
            for video in videos_details['items']:
                if 'liveStreamingDetails' in video:
                    if video.get('snippet', {}).get('liveBroadcastContent') == 'live':
                        live_streams.append({
                            'id': video['id'],
                            'title': video['snippet']['title'],
                            'thumbnail': video['snippet']['thumbnails']['high']['url'],
                            'url': f"https://www.youtube.com/watch?v={video['id']}"
                        })
                    elif video.get('snippet', {}).get('liveBroadcastContent') == 'upcoming':
                        if 'scheduledStartTime' in video['liveStreamingDetails']:
                            start_time = video['liveStreamingDetails']['scheduledStartTime']
                            upcoming_streams.append({
                                'id': video['id'],
                                'title': video['snippet']['title'],
                                'thumbnail': video['snippet']['thumbnails']['high']['url'],
                                'scheduled_time': start_time,
                                'url': f"https://www.youtube.com/watch?v={video['id']}"
                            })
            
            return {
                "live": live_streams if live_streams else False,
                "upcoming": upcoming_streams
            }
        
        return {"live": False, "upcoming": []}
