import requests
import os
import csv

API_KEY = '7bcc522382eda8a7d222068e30fa853c'
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

# Create folder for album covers
os.makedirs("album_covers", exist_ok=True)

with open("files/top_500.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        artist = row["artist"]
        album = row["name"]
        params = {
            "method": "album.getinfo",
            "api_key": API_KEY,
            "artist": artist,
            "album": album,
            "format": "json"
        }

        try:
            response = requests.get(BASE_URL, params=params)
            data = response.json()
            images = data["album"].get("image", [])
            # Try to get the largest image
            if images:
                image_url = images[-1]["#text"]
                if image_url:
                    image_data = requests.get(image_url).content
                    filename = f'album_covers/{row["position"]}_{artist}_{album}.jpg'.replace("/", "-")
                    with open(filename, 'wb') as f:
                        f.write(image_data)
                        print(f"Saved: {filename}")
        except Exception as e:
            print(f"Error fetching {artist} - {album}: {e}")
