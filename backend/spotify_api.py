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
    """
    Search for tracks on Spotify based on a query in the format 'Title by Artist'.
    Returns a list of tracks or an empty list if no results are found.
    """
    try:
        # Initialise title and artist
        title = ""
        artist = ""

        # Split query into title and artist using last occurrence of the word 'by',
        parts = query.rsplit(' by ', 1)
        title = parts[0].strip()
        artist = parts[1].strip()

        # Build the Spotify search query
        if title and artist:
            sanitised_query = f"track:{title} artist:{artist}"
        else:
            sanitised_query = f"track:{title}"

        results = sp.search(q=sanitised_query, type='track', limit=1)
        
        return results['tracks']['items']
    
    except Exception as e:
        print(f"Error searching Spotify: {e}")
        return []
