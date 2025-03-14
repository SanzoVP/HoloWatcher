# HoloWatcher 


## Setup Instructions

Make sure you have at least python 3.12.2 installed

Have at least Windows 10 TH2 10586 for the funny colors otherwise good luck reading it

### Setting up YouTube API

1. Download the [Latest Release](https://github.com/SanzoVP/HoloWatcher/releases/latest) and unzip it
2. Go to the [Google Cloud Console](https://console.cloud.google.com/)
3. Create a new project
4. Enable the YouTube Data API v3
5. Go to "Credentials" and create an OAuth client ID
6. Choose "Desktop application" as the application type
    - During the setup, you’ll be asked to publish the app. You can either go through Google’s verification process 
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

If you want you can do windows+r and type `shell:startup` and then add a shortcut to the run.bat to automatically start it up, you do have to type in auto and leave it running in the background

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

## More stuff if you care

I'm probably mostly done with this but if there is a new version you can go into the build folder and then holowatcher folder and then the subscriptions.json, so like `build\HoloWatcher\data\subscriptions.json` to copy over your subscriptions if you don't want to set them up again.

I'll be making new versions for the newer members or if I missed any but other than that it should be fine to use the same version.