import os
import csv
from googleapiclient.discovery import build

# Add the API key
API_KEY = 'INSERT_API_KEY_HERE'

# Add the YouTube playlist ID
PLAYLIST_ID = 'INSERT_PLAYLIST_ID_HERE'

# Script function
def YtToCsv (API_KEY, PLAYLIST_ID):
	# Add the YouTube API client
	youtube = build('youtube', 'v3', developerKey=API_KEY)

	# Variables for the paginated results. YT sends max 50 results at a time
	nextPageToken = None
	videosInfo = []

	# Get all playlist items
	while True:
		playlistItems = youtube.playlistItems().list(
			part='contentDetails,snippet',
			playlistId=PLAYLIST_ID,
			maxResults=50,
			pageToken=nextPageToken
		).execute()

		# Add videos to playlistItems
		videosInfo.extend(playlistItems['items'])

		# Check for the next page
		nextPageToken = playlistItems.get('nextPageToken')

		# Break the loop if there aren't anymore pages
		if not nextPageToken:
			break

	# Variable for storing all the song data
	tracksList = []

	# Get the song and artist names and add it to the tracksList
	for video in videosInfo:
		title = video['snippet']['title']
		if title == 'Deleted video' or title == 'Private video':    # Check if video is deleted or private
			continue
		channelTitle = video['snippet']['videoOwnerChannelTitle']

		# Check whether the artist's name is present in the title
		if ' - ' in title:
			titleParts = title.split(' - ')
			artist = titleParts[0].strip()
			songName = titleParts[1].strip()
		else:
			# Use the channel title as artist name if the artist name is not present in the title
			artist = channelTitle
			songName = title

		tracksList.append({'Artist': artist, 'Title': songName})

	# Get the playlist info
	playlistInfo = youtube.playlists().list(
		part='snippet',
		id=PLAYLIST_ID
	).execute()

	# Get the playlist title and use that as the csv file name
	playlistTitle = playlistInfo['items'][0]['snippet']['title']
	csvFilename = f'{playlistTitle} [playlist].csv'
	csvPath = os.path.join(os.getcwd(), csvFilename)

	# Write tracksList into a CSV file
	with open(csvPath, 'w', newline='', encoding='utf-8') as csv_file:
		fieldnames = ['Artist', 'Title']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

		writer.writeheader()
		writer.writerows(tracksList)

	print(f'Playlist data saved to {csvFilename}')

YtToCsv(API_KEY, PLAYLIST_ID)