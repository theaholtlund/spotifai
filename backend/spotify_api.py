# Import required libraries
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import logging

# Setup for logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

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
    logging.critical("Failed to authenticate Spotify client.", exc_info=True)
    raise e

def search_tracks(query):
    """Search for tracks on Spotify based on a query input of title and artist."""
    try:
        parts = query.rsplit(' by ', 1)
        if len(parts) != 2:
            logging.warning(f"Invalid query format: {query}")
            return []

        title, artist = parts
        sanitised_query = f"track:{title.strip()} artist:{artist.strip()}"

        results = sp.search(q=sanitised_query, type='track', limit=1)
        tracks = results.get('tracks', {}).get('items', [])
        return tracks
    except Exception as e:
        logging.error(f"Error searching Spotify: {e}")
        return []
