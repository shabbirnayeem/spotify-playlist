from bs4 import BeautifulSoup
import requests
import spotipy
from pprint import pprint


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM--DD: ")


# https://www.billboard.com/charts/{date}?rank=1
# Getting the billboard.com html page
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
# saving HTML data to data
data = response.text

# using Beautiful Soup to scrape the HTML data
soup = BeautifulSoup(data, "html.parser")

# parsing to get the song titles
song_title = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")

# using spotipy to authenticate to spotify
headers = spotipy.oauth2.SpotifyOAuth(client_id="[YOUR ID]",
                            client_secret="[YOUR SECRET]",
                            redirect_uri="http://example.com",
                            scope="playlist-modify-private",
                            cache_path=".cache")

# getting current user information
spotipy_user = spotipy.Spotify(auth_manager=headers)
# getting hold of the user ID, need to create the play list
user_id = spotipy_user.current_user()["id"]

# authenticating to spotify using the headers data
sp = spotipy.client.Spotify(auth_manager=headers)

# getting hold of the year from the user input
YYYY = date.split("-")[0]

# creating a list of song uri
song_uri = []
for song_name in song_title:

    try:
        # using the search function from spotipy to search for each song title
        result = sp.search(f"track:{song_name.getText()} year:{YYYY}")
        # getting hold of each song uri
        uri = result['tracks']['items'][0]['uri']
    except IndexError:
        # if song not found in spotify skip and continue to the next
        continue
    else:
        # append each uri to song_uri list
        song_uri.append(uri)

# print(len(song_uri))

# Creating a private playlist in spotify
playlist = sp.user_playlist_create(user=user_id,
                        name=f"{date} Billboard 100",
                        public=False,
                        collaborative=False,
                        description="Creating playlist with python code")

play_list_id = playlist["id"]

# adding all the songs from the billboard to the playlist
# note items take a list tracks
sp.playlist_add_items(playlist_id=play_list_id,
                      items=song_uri,
                      position=None)

