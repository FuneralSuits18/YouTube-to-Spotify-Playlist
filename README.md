## yt-to-csv.py

Converts a YouTube playlist's tracks into a .csv file.

#### Instructions

1. Get an API key from the Google developer console
2. Get the playlist id. The playlist must be public
3. Download the script
4. Run: pip install google-api-python-client
5. In the script, insert the API key and the playlist ID and run.

## csv-to-spotify.py
Adds tracks to a playlist from a csv file with format: Title,Artist

*Problems:*  
*If the CSV file contains duplicates, the script will add the song multiple times.*  
*Adds the first search result in Spotify. Will attempt to refine it later.*


## remove-all-tracks-from-playlist.py
Removes all the tracks from a playlist.

*Problems:*  
*Need to run the script multiple times if the playlist is big. Don't know how to solve the problem. Deleting the playlist is just simpler and more efficient.*
