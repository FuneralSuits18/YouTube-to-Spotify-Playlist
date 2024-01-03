
# ! Didn't check for duplicates in the csv. Should implement checking for duplicates right before adding. But might slow down the script even more.
# ! Adds the first found search result in Spotify 🫠🫠

import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from requests.exceptions import ReadTimeout

# Add authorization
SPOTIPY_CLIENT_ID = 'SPOTIFY_CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'SPOTIFY_CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'     # Add this in the spotify dashboard app as well. Where the redirection takes doesn't matter in this script because this is just a placeholder

# Add the Spotify playlist ID
SPOTIFY_PLAYLIST_ID = 'SPOTIFY_PLAYLIST_ID'

# Set the path to your CSV file. The file must be in format "title, artist"
csvPath = 'PATH/FILENAME'

# Function to run the script
def updatePlaylist(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIFY_PLAYLIST_ID, SPOTIPY_REDIRECT_URI, csvPath):
    # Add the scope for the Spotify API
    modifyScope = 'playlist-modify-public playlist-modify-private'    # ! Check why only 'playlist-modify-public' didn't work 🤨

    # Authenticate with Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=modifyScope))

    # Variable to store all the tracks from the .csv file
    csvTracks = []

    # Read from the .csv file
    with open(csvPath, 'r', encoding='utf-8') as csvFile:
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:
            csvTracks.append({'Artist': row['Artist'], 'Title': row['Title']})

    # Get the track list from the playlist
    spotifyTracks = sp.playlist_tracks(SPOTIFY_PLAYLIST_ID, fields='items(track(id))')['items']

    # Get track ids to check for duplicity
    spotifyTrackIds = [track['track']['id'] for track in spotifyTracks]

    # Keep track of successfully added tracks 😌
    addedTracks = []

    # Keep track of tracks that are already in the playlist to delete from the .csv file later
    inSpotifyPlaylist = []

    # Search tracks on Spotify and add to the playlist if not already in the playlist
    for track in csvTracks:
        title = track['Title']
        artist = track['Artist']

        # Search for the track on Spotify
        result = sp.search(q=f'{title} {artist}', type='track', limit=1)

        # Check if the track present in search
        if result['tracks']['items']:
            trackUri = result['tracks']['items'][0]['uri']

            # Check if the track is already in the playlist
            if trackUri not in spotifyTrackIds:
                # Add the track to the playlist
                try:
                    sp.playlist_add_items(SPOTIFY_PLAYLIST_ID, [trackUri])
                    print(f"Added '{title}' by {artist} to the playlist.")
                    addedTracks.append(track)
                except ReadTimeout as e:
                    print(f"Request timed out for '{artist} - {title}': {e}")
            else:
                print(f"Skipped '{artist} - {title}' as it is already in the playlist.")
                inSpotifyPlaylist.append(track)

    # Remove successfully added and already in the playlist tracks from the CSV file
    for addedTrack in addedTracks + inSpotifyPlaylist:
        csvTracks.remove(addedTrack)

    with open(csvPath, 'w', newline='', encoding='utf-8') as csvFile:
        fieldnames = ['Title', 'Artist']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csvTracks)

    print("Playlist update complete.")

# Run the script
updatePlaylist(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIFY_PLAYLIST_ID, SPOTIPY_REDIRECT_URI, csvPath)
