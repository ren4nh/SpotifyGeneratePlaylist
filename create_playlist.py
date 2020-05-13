import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

from exceptions import ResponseException


class CreatePlaylist:
    def __init__(self):
        self.playlist_name = input("Enter the playlist name : ")
        self.playlist_description = input("Enter the playlist description : ")
        self.spotify_user_id = input("Enter your Spotify user id : ")
        self.spotify_token = input("Enter your Spotify OAuth token : ")
        self.playlist_id = input("Enter your Youtube playlist id : ")
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    def get_youtube_client(self):
        """ Log Into Youtube, Copied from Youtube Data API """
        api_service_name = "youtube"
        api_version = "v3"

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey="AIzaSyB98OglUIerOjnqfU2hpkgAji2OoYyGzx4")

        return youtube_client

    def get_playlist_videos(self):
        print("[youtube] Getting playlist videos info")
        """Grab Our Playlist Videos & Create A Dictionary Of Important Song Information"""
        request = self.youtube_client.playlistItems().list(
            part="snippet, contentDetails",
            playlistId=self.playlist_id,
            maxResults=50
        )

        options = {"ignoreerrors":"True", "format":"worst", "quiet":"True"}

        while request:
            # while request:
            response = request.execute()

            # collect each video and get important information
            for item in response["items"]:
                video_title = item["snippet"]["title"]
                youtube_url = "https://www.youtube.com/watch?v={}".format(
                    item["snippet"]["resourceId"]["videoId"])

                # use youtube_dl to collect the song name & artist name
                video = youtube_dl.YoutubeDL(options).extract_info(
                    youtube_url, download=False)

                if video is not None:
                    song_name = video["track"]
                    artist = video["artist"]

                    if song_name is not None and artist is not None:
                        spotify_uri = self.get_spotify_uri(song_name, artist)
                        if spotify_uri is not None:
                            # save all important info and skip any missing song and artist
                            self.all_song_info[video_title] = {
                                "youtube_url": youtube_url,
                                "song_name": song_name,
                                "artist": artist,

                                # add the uri, easy to get song to put into playlist
                                "spotify_uri": spotify_uri

                            }
                else:
                    print("[youtube] Cannot extract song info for the video {}".format(youtube_url))
            request = self.youtube_client.playlistItems().list_next(request, response)

    def create_playlist(self):
        print("[spotify] Creating a Spotify playlist")
        request_body = json.dumps({
            "name": self.playlist_name,
            "description": self.playlist_description,
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            self.spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        return response_json["id"]

    def get_spotify_uri(self, song_name, artist):
        """Search For the Song"""
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        
        uri = None
        if len(songs) > 0:
            uri = songs[0]["uri"]
        else:
            print("[spotify] Cannot find this song {} - {}".format(song_name, artist))

        return uri

    def add_song_to_playlist(self):
        
        """Add all playlist songs into a new Spotify playlist"""
        # populate dictionary with our liked songs
        self.get_playlist_videos()

        # collect all of uri
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]

        
        # create a new playlist
        playlist_id = self.create_playlist()

        print("[spotify] Adding songs to Spotify playlist ...")

        # add all songs into new playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        # check for valid response status
        if response.status_code != 201:
            raise ResponseException(response.status_code)

        response_json = response.json()
        print("[spotify] Songs addded")


if __name__ == '__main__':
    cp = CreatePlaylist()
    print("[app] Starting ...")
    cp.add_song_to_playlist()
    print("[app] Finish")
