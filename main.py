import configparser
import json
import requests
import sys

def get_info(QUERIES, CLIENT_ID, CLIENT_SECRET):

    # Get the access token
    auth_response = requests.post("https://accounts.spotify.com/api/token",
                                data={
                                    "grant_type": "client_credentials"
                                },
                                auth=(CLIENT_ID, CLIENT_SECRET))

    # If the authentification was succesful, get information about tracks

    results = {}

    if auth_response.status_code == 200:
        access_token = auth_response.json()["access_token"]

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        }

        for QUERY in QUERIES:

            results[QUERY] = None

            search_response = requests.get(
                f"https://api.spotify.com/v1/search?q={QUERY}&type=track",
                headers=headers
            )

            # Check if the request was successful
            if search_response.status_code == 200:
                # Parse the JSON data
                data = search_response.json()
                track = None
                try:
                    # Get the first track in the list of returned tracks
                    track = data["tracks"]["items"][0]
                except:
                    print(f"\nWARNING: No track was found for the specified query: {QUERY}\n")

                if track != None:
                    
                    # Get the track name, artist(s) & album IDs
                    track_name = track["name"]
                    track_artists = {artist["name"]:artist["id"] for artist in track["artists"]}
                    track_id = track["id"]
                    album_id = track["album"]["id"]
                    print(f"\nTrack: {track_name} by {', '.join(track_artists.keys())}\n--> Track ID: {track_id}\n--> Album ID: {album_id}")


                    # Get information about the album
                    album = track["album"]
                    album_name = album["name"]
                    release_date = album["release_date"]
                    url_cover = album["images"][0]["url"]
                    print(f"--> Name of the album: {album_name}\n--> Release Date: {release_date}\n--> Cover URL: {url_cover}")


                    # Get the genres associated to each artist
                    all_genres = []
                    print("--> Artist(s)'s genres:")
                    for artist, id in track_artists.items():
                        # Get information about the track
                        artist_response = requests.get(f"https://api.spotify.com/v1/artists/{id}", headers=headers)
                        if artist_response.status_code == 200:
                            artist_data = artist_response.json()
                            genres = artist_data["genres"]
                            all_genres.extend(genres)
                        else:
                            print(f"Failed to get track information: {artist_response.json()}")

                        print(f"\t{artist}: {genres}")
                    
                    all_genres = set(all_genres)
                    print("--> Genres: ", " - ".join([genre for genre in all_genres]))

                    results[QUERY] = [album_name, release_date, url_cover, all_genres]

            else:
                print("Track search failed with status code", search_response.status_code)

    else:
        print(f"Failed to get access token: {auth_response.json()}")

    return results




if __name__ == '__main__':

    # The Spotify Web API requires authentication, using the OAuth 2.0 Authorization Framework
    # Load the Spotify API credentials from the configuration file
    CONFIG = configparser.ConfigParser()
    CONFIG.read("./config.ini")
    CLIENT_ID = CONFIG["DEFAULT"]["client_id"]
    CLIENT_SECRET = CONFIG["DEFAULT"]["client_secret"]

    DEFAULT_QUERY = ["Aegis - Andre Bratten"]
    QUERIES = []

    if len(sys.argv) == 1:      
        print(f"\nWARNING: No query was given. The default query '{DEFAULT_QUERY}' will be used.\n")
        QUERIES = DEFAULT_QUERY
    else:
        for i in range(1, len(sys.argv)):
            QUERIES.append(sys.argv[i])

    infos = get_info(QUERIES, CLIENT_ID, CLIENT_SECRET)
    print("\n\n", infos)

