# HoloWatcher - Setup Instructions

## Setting up YouTube API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the YouTube Data API v3
4. Go to "Credentials" and create an OAuth client ID
5. Choose "Desktop application" as the application type
6. Download the JSON file and rename it to `client_secrets.json`
7. Place the file in the same directory as the application and make sure it's formatted like `client_secrets.json.example`
    - it should be in the build folder where the example also is

## Open the app
- Open it by running the run.bat file, it should handle everything correctly
    - If not please report it as a bug in [Bug Reports](https://github.com/SanzoVP/HoloWatcher/issues)

## First Run

- On first run, the application will open a browser window
- Sign in with your Google account and grant the requested permissions
- Your credentials will be saved as `token.pickle` for future use

## Go wild
Subscribe to whoever you want, list will be updated if I remember to.

### Commands
- action: commands
- To subscribe: sub, subscribe
- To check for streams: check, lives, check lives
- To reset visited streams: del, delete
- To check who you are subscribed to: list, view, subs, subscriptions
- To automate checking for streams: auto, automation