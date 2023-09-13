import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import csv
from decouple import config
import time

CLIENT_ID = config("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = config("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = config("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-read-recently-played",
    )
)

csv_file = "song_history.csv"

# Check if the file exists, and create headers if not
try:
    with open(csv_file, mode="r") as file:
        pass
except FileNotFoundError:
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        headers = [
            "Song Name",
            "Artist(s)",
            "Acousticness",
            "Danceability",
            "Duration (ms)",
            "Energy",
            "Instrumentalness",
            "Key",
            "Liveness",
            "Loudness",
            "Mode",
            "Speechiness",
            "Tempo",
            "Time Signature",
            "Valence",
        ]
        writer.writerow(headers)

# Load existing data from the CSV file to avoid duplicates
existing_songs = set()
with open(csv_file, mode="r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        existing_songs.add((row[0], row[1]))

# Continuously log songs
while True:
    recently_played = sp.current_user_recently_played(limit=50)

    song_data = []
    for item in recently_played["items"]:
        track = item["track"]
        song_name = track["name"]
        artists = ", ".join([artist["name"] for artist in track["artists"]])

        if (song_name, artists) not in existing_songs:
            features = sp.audio_features([track["uri"]])[0]

            song_data.append(
                [
                    song_name,
                    artists,
                    features["acousticness"],
                    features["danceability"],
                    features["duration_ms"],
                    features["energy"],
                    features["instrumentalness"],
                    features["key"],
                    features["liveness"],
                    features["loudness"],
                    features["mode"],
                    features["speechiness"],
                    features["tempo"],
                    features["time_signature"],
                    features["valence"],
                ]
            )
            existing_songs.add((song_name, artists))

    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(song_data)

    print(f"Logged {len(song_data)} new songs to {csv_file}")

    # Sleep for 3 minutes before checking again
    time.sleep(180)
