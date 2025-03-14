# VTuber Tracker - Setup Instructions

## Setting up YouTube API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the YouTube Data API v3
4. Go to "Credentials" and create an OAuth client ID
5. Choose "Desktop application" as the application type
6. Download the JSON file and rename it to `client_secrets.json`
7. Place the file in the same directory as the application

## First Run

- On first run, the application will open a browser window
- Sign in with your Google account and grant the requested permissions
- Your credentials will be saved as `token.pickle` for future use