
# ! Need to run the script multiple times if the playlist is big. Don't know how to solve the problem 😔😔😔. (Made a delay for response but no luck. Maybe the problem is from Spotify side?)

import requests
import base64
import webbrowser
from urllib.parse import urlparse, parse_qs

# Set Spotify things
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
# ! Check if works for private playlists. It should.
PLAYLIST_ID = 'PLAYLIST_ID'
REDIRECT_URI = 'http://localhost:8888/callback'  # Add in the Spotify app as well

SCOPE = 'playlist-modify-public playlist-modify-private'    # ! Check why this doesn't work if set to only playlist-modify-public even when I'm using a public playlist.

# Get access token
def get_access_token(client_id, client_secret, redirect_uri, scope):
    auth_url = 'https://accounts.spotify.com/authorize'
    token_url = 'https://accounts.spotify.com/api/token'

    # Request user authorization
    auth_url_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope
        
    }
    auth_response = requests.get(auth_url, params=auth_url_params)

    # Open url in browser
    webbrowser.open(auth_response.url)

    print('Please login to Spotify and authorize the application.')

    # Take the whole link and process to get the authorization code
    redirect_uri_with_code = input('Copy-paste the whole link: ')
    parsed_url = urlparse(redirect_uri_with_code)
    auth_code = parse_qs(parsed_url.query).get('code')

    # Request access token
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')
    }
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
    }

    token_response = requests.post(token_url, headers=headers, data=data)
    
    if token_response.status_code == 200:
        return token_response.json().get('access_token')
    else:
        raise Exception(f"Failed to get access token. Status code: {token_response.status_code}, Response: {token_response.text}")


# Remove all tracks from the playlist
def remove_all_tracks(playlist_id, access_token):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    while True:
        # Get the current tracks in the playlist
        response = requests.get(url, headers=headers)
        response_json = response.json()
        current_tracks = response_json.get('items', [])

        # Check if tracks exist
        if not current_tracks:
            break

        # Get the track URIs
        track_uris = [{'uri': track['track']['uri']} for track in current_tracks]

        # Prepare the request payload
        data = {'tracks': track_uris}

        # Remove tracks from the playlist
        response = requests.delete(url, headers=headers, json=data)

        if response.status_code == 200:
            print(f"Removed {len(track_uris)} tracks from the playlist with ID: {playlist_id}")
        else:
            print(f"Failed to remove tracks. Status code: {response.status_code}, Response: {response.text}")

        # Check for the next page
        url = response_json.get('next')
        if not url:
            break
        

# Main script
try:
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE)
    remove_all_tracks(PLAYLIST_ID, access_token)
except Exception as e:
    print(f"Error: {e}")