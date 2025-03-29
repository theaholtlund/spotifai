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


def search_tracks(song_name: str, retries: int = 3, delay: int = 1) -> List[Dict[str, str]]:
    """Search for tracks on Spotify based on a query input of title and artist."""
    try:
        # Split the song_name to separate title and artist
        parts = song_name.split(' - ')

        # Check if the song_name format is valid (must contain exactly one ' - ')
        if len(parts) != 2:
            logging.warning(f"Invalid query format: {song_name}")
            return []

        title, artist = parts
        search_query = f"track:{title.strip()} artist:{artist.strip()}"

        logging.info(f"Searching for track: {song_name}")
        results = sp.search(q=search_query, type='track', limit=1)
        return results.get('tracks', {}).get('items', [])

    except spotipy.exceptions.SpotifyException as e:
        # Handle rate limit exceptions and retry if necessary
        if retries > 0 and 'rate limit exceeded' in str(e).lower():
            logging.warning(
                f"Spotify rate limit exceeded, retrying in {delay} seconds...")
            time.sleep(delay)  # Wait before retrying
            # Retry with increased delay
            return search_tracks(song_name, retries - 1, delay * 2)
        else:
            logging.error(f"Spotify API error: {e}", exc_info=True)
            return []
    except Exception as e:
        logging.error(f"Error searching for track: {song_name}, {e}", exc_info=True)
        return []


def search_public_playlists_by_name(names):

    for name in names:
        try:
            logging.info(f"Searching for playlist: {name}")
            results = sp.search(q=name, type='playlist', limit=1)
            return results

        except Exception as e:
            logging.error(
                f"Error searching for playlist: {name}, {e}", exc_info=True)
            return []
