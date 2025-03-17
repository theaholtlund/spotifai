# Import required libraries
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import logging
import time

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Spotify authentication
try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
    ))
    logging.info("Spotify client successfully authenticated.")
except Exception as e:
    logging.critical("Failed to authenticate Spotify API", exc_info=True)
    raise e

def search_tracks(song_name, retries=3, delay=1):
    """Search for tracks on Spotify based on a query input of title and artist."""
    try:
        parts = song_name.split(' - ')
        if len(parts) != 2:
            logging.warning(f"Invalid query format: {song_name}")
            return []

        title, artist = parts
        search_query = f"track:{title.strip()} artist:{artist.strip()}"

        logging.info(f"Searching for track: {song_name}")
        results = sp.search(q=search_query, type='track', limit=1)
        return results.get('tracks', {}).get('items', [])

    except spotipy.exceptions.SpotifyException as e:
        if retries > 0:
            return search_tracks(song_name, retries - 1, delay * 2)
        else:
            return []
    except Exception as e:
        logging.error(f"Spotify search error: {e}", exc_info=True)
        return []
