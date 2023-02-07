import requests
import json
import configparser

# The Spotify Web API requires authentication, using the OAuth 2.0 Authorization Framework

# Load the Spotify API credentials from the configuration file
config = configparser.ConfigParser()
config.read("./config.ini")
client_id = config["DEFAULT"]["client_id"]
client_secret = config["DEFAULT"]["client_secret"]

# Get the access token
auth_response = requests.post("https://accounts.spotify.com/api/token",
                              data={
                                  "grant_type": "client_credentials"
                              },
                              auth=(client_id, client_secret))

if auth_response.status_code == 200:
    access_token = auth_response.json()["access_token"]

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    query = "track:aegis artist:andre bratten"

    search_response = requests.get(
        f"https://api.spotify.com/v1/search?q={query}&type=track",
        headers=headers
    )

    track_id = ""

    # Check if the request was successful
    if search_response.status_code == 200:
        # Parse the JSON data
        data = search_response.json()

        # Get the first track in the list of tracks
        try:
            track = data["tracks"]["items"][0]

            # Get the track name, artist(s) & ID
            track_name = track["name"]
            track_artists = [artist["name"] for artist in track["artists"]]
            track_id = track["id"]
            album_id = track["album"]["id"]

            print(f"Track: {track_name} by {', '.join(track_artists)} --> Track ID: {track_id} // Album ID: {album_id}")
        except:
            print("No track was found the specified query")

    else:
        print("Search failed with status code", search_response.status_code)

    if track_id != "":
        '''
        # Get information about the track
        track_response = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)

        if track_response.status_code == 200:
            track_data = track_response.json()
            print(json.dumps(track_data, indent=4))

        else:
            print(f"Failed to get track information: {track_response.json()}")
        '''

        # Get information about the album
        album_response = requests.get(f"https://api.spotify.com/v1/albums/{album_id}", headers=headers)

        if album_response.status_code == 200:
            album_data = album_response.json()
            
            url_cover = album_data["images"][0]["url"]
            genres = album_data["genres"]
            release_date = album_data["release_date"]

            print(f"URL of the cover: {url_cover}\nGenres: {genres}\nRealease Date: {release_date}")

        else:
            print(f"Failed to get album information: {album_response.json()}")

        
    else:
        print("No track ID was found")

else:
    print(f"Failed to get access token: {auth_response.json()}")