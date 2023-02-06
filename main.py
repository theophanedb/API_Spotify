import requests
import json

# Replace <client_id> and <client_secret> with your Spotify API credentials
client_id = "<client_id>"
client_secret = "<client_secret>"

# Get the access token
auth_response = requests.post("https://accounts.spotify.com/api/token",
                              data={
                                  "grant_type": "client_credentials"
                              },
                              auth=(client_id, client_secret))

if auth_response.status_code == 200:
    access_token = auth_response.json()["access_token"]
    headers = {
        "Authorization": "Bearer " + access_token
    }

    # Replace <track_id> with the id of the track you want information about
    track_id = "<track_id>"

    # Get information about the track
    track_response = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)

    if track_response.status_code == 200:
        track_data = track_response.json()
        print(json.dumps(track_data, indent=4))
    else:
        print(f"Failed to get track information: {track_response.json()}")
else:
    print(f"Failed to get access token: {auth_response.json()}")