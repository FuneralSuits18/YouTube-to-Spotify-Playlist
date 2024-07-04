## yt-to-csv.py

Gets the info from a YouTube playlist and lists the tracks into a .csv file.

**Instructions:**
1. Get an API key from the Google developer console
2. Get the id of the playlist. The playlist must be public
3. In the script, insert the API key and the playlist ID.
4. Run: `pip install -r requirements.txt`
5. Run the script.


## csv-to-spotify.py
Adds tracks to a playlist from a csv file with format: Title,Artist

**Instructions:**
1. Create an app in Spotify Developer Dashboard.
2. Get client ID and client secret from settings
3. Set a redirect URI: for example, `http://localhost:8888/callback`  
The script doesn't actually use this URI.
4. Get the ID of the playlist you want the script to add songs to.
5. Get the path to the csv file.
5. Insert the values in the script.
6. Run: `pip install -r requirements.txt`
7. Run the script.


## remove-all-tracks-from-playlist.py
Removes all the tracks from a playlist.

Instructions are similar to the last one.


### *Problems:*  
*csv-to-spotify.py:*
- *If the CSV file contains duplicates, the script will add the song multiple times.*  
- *Adds the first search result in Spotify. Will attempt to refine it later.*

*remove-all-tracks-from-playlist.py:*
- *Need to run the script multiple times if the playlist is big. Don't know how to solve the problem. Deleting the playlist is just simpler and more efficient.*