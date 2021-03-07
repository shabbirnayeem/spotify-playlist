# spotify-playlist
100daysofcode-day75_76


## Project Description:
Music time machine, in this project we are going to transfer back in time through music. Using billboard hot 100 lists from any time in history and add these tracks to your Spotify playlist.

## Modules used:
  - Python Request Libarrby: to get the HTML data
  - Python BeautifulSoup: to parse the HTML data
  - spotipy: to work with spotify API

# Use case:
To use this all you have to do is enter any date in YYYY-MM-DD format and it gets the top 100 songs from that day from the https://www.billboard.com/charts/hot-100. The program searches Spotify for each of these tracks and if they exit in Spotify it will take playlist with a given date and add tracks.



## Step 1:
Use python request library to get the HTML data from https://www.billboard.com/charts/hot-100/

```
# user input, ask the user to pick a date
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM--DD: ")
# getting hold of the year from the user input
# this will be helpful to search in Spotify
YYYY = date.split("-")[0]

# Getting the billboard.com html page
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
# saving HTML data to data
data = response.text
```

## Step 2:
Use Beautiful Soup to scrape the HTML data and get the song_title from the billboard website.
Use the title to search spotify.

```
# using Beautiful Soup to scrape the HTML data
soup = BeautifulSoup(data, "html.parser")

# parsing to get the song titles
song_title = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")
```

## Step 3:
Use the spotipy module to authenticate to Spotify. Spotipy basically makes it easy to work with Spotify API.
In order to create a playlist in Spotify, you must have an account with Spotify.
Once you've signed up/ signed in, go to the developer dashboard and create a new Spotify App, here you can find your ID and Secret.

Learn more about spotipy module: https://spotipy.readthedocs.io/en/2.17.1/

```
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
```

# Step 4:
Use Spotipy to search Spotify for all songs to got from the billboard website.
Each track in Spotify has a unique URI, we hold of this and create a list of all 100 URI.

```
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

```

## Step 5:
Creating the playlist in Spotify.
All we have to do use the spotipy create playlist function and pass in the following info:
  - User ID
  - Name of the playlist
  - Public or Private
  - Description

```
# Creating a private playlist in spotify
playlist = sp.user_playlist_create(user=user_id,
                        name=f"{date} Billboard 100",
                        public=False,
                        collaborative=False,
                        description="Creating playlist with python code")
                        
# get hold of the unique playlist ID, this is required in the next step to add tracks to the playlist.
play_list_id = playlist["id"]
```


## Step 6:
Adding tracks to the playlist.
Use the playlist_add_items function of spotipy and pass in the following:
  - Playlist ID
  - uri
 
```
# adding all the songs from the billboard to the playlist
# note items take a list tracks
sp.playlist_add_items(playlist_id=play_list_id,
                      items=song_uri,
                      position=None)
```
