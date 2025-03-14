# HoloWatcher 


## Setup Instructions

Make sure you have at least python 3.12.2 installed 

### Setting up YouTube API

1. Download the [Latest Release](https://github.com/SanzoVP/HoloWatcher/releases/latest) and unzip it
2. Go to the [Google Cloud Console](https://console.cloud.google.com/)
3. Create a new project
4. Enable the YouTube Data API v3
5. Go to "Credentials" and create an OAuth client ID
6. Choose "Desktop application" as the application type
7. Download the JSON file and rename it to `client_secrets.json`
8. Place the file in the same directory as the application and make sure it's formatted like `client_secrets.json.example`
    - It should be in the **`build`** folder where the example also is

### Open the app
- Open it by running the run.bat file, it should handle everything correctly
    - If not please report it as a bug in [Bug Reports](https://github.com/SanzoVP/HoloWatcher/issues)

### First Run

- On first run, the application will open a browser window
- Sign in with your Google account and grant the requested permissions
- Your credentials will be saved as `token.pickle` for future use

### Go wild
Subscribe to whoever you want, list will be updated if I remember to.

#### Commands
- action: `commands`
- To subscribe: `sub`, `subscribe`
- To check for streams: `check`, `lives`, `check lives`
- To reset visited streams: `del`, `delete`
- To check who you are subscribed to: `list`, `view`, `subs`, `subscriptions`
- To automate checking for streams: `auto`, `automation`

## What and why?

HoloWatcher is a program that you are supposed to let run in the background, it will open a new tab to any Hololive members stream that you are subscribed to. (In the program not on youtube) 

This is so you never miss a stream again no matter what you are doing. (You should probably turn it off while playing a game or doing something important so it doesn't distract you ^w^)

Why did I do this? idk I thought the idea of just doing something just to be suprised by a random stream out of no where was funny and that it would be a good learning experience