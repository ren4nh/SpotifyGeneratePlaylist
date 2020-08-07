# SpotifyGeneratePlaylist
A simple script that takes videos from a public playlist on Youtube, and generates a Spotify playlist based on that songs.

## Table of Contents
* [Technologies](#Technologies)
* [Setup](#LocalSetup)
* [Troubleshooting](#Troubleshooting)

## Technologies
* [Youtube Data API v3]
* [Spotify Web API]
* [Requests Library v 2.22.0]
* [Youtube_dl v 2020.03.24]

## LocalSetup
1) Install All Dependencies   
`pip3 install -r requirements.txt`

2) Collect You Spotify User ID and Oauth Token From Spotfiy and add it to secrets.py file
    * To Collect your User ID, Log into Spotify then go here: [Account Overview] and its your **Username**
    ![alt text](images/userid.png)
    * To Collect your Oauth Token, Visit this url here: [Get Oauth] and click the **Get Token** button
    ![alt text](images/spotify_token.png)

4) Run the File  
`python3 create_playlist.py`

## Troubleshooting
* Spotify Oauth token expires very quickly, If you come across a `KeyError` this could
be caused by an expired token. So just refer back to step 3 in local setup, and generate a new
token!  
* Sometimes youtube_dl lib cannot extract the video info


   [Youtube Data API v3]: <https://developers.google.com/youtube/v3>
   [Spotify Web API]: <https://developer.spotify.com/documentation/web-api/>
   [Requests Library v 2.22.0]: <https://requests.readthedocs.io/en/master/>
   [Account Overview]: <https://www.spotify.com/us/account/overview/>
   [Youtube_dl v 2020.03.24]:<https://github.com/ytdl-org/youtube-dl/>
