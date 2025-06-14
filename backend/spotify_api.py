# Import required libraries
import os
import time
import logging
from typing import List, Dict

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Authenticate with Spotify
try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    ))

    logging.info("Spotify client authenticated successfully.")
except Exception:
    logging.critical("Failed to authenticate with Spotify API.", exc_info=True)
    raise


def search_spotify_tracks(song_name: str, retries: int = 3, delay: int = 1) -> List[Dict]:
    """Search for a Spotify track based on query input of title and artist."""
    if ' - ' not in song_name:
        logging.warning(f"Invalid song name format, expected 'Title - Artist': {song_name}")
        return []

    title, artist = map(str.strip, song_name.split(' - ', 1))
    query = f"track:{title} artist:{artist}"

    for attempt in range(retries):
        try:
            logging.info(f"Searching Spotify for track: {song_name}")
            result = sp.search(q=query, type='track', limit=1)
            return result.get('tracks', {}).get('items', [])
        except spotipy.exceptions.SpotifyException as e:
            msg = str(e).lower()
            if 'rate limit' in msg:
                wait_time = delay * (2 ** attempt)
                logging.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logging.error(f"Spotify API error while searching track '{song_name}': {e}", exc_info=True)
                break
        except Exception as e:
            logging.error(f"Unexpected error during track search '{song_name}': {e}", exc_info=True)
            break

    return []


def search_public_playlists_by_name(names: List[str], retries: int = 3, delay: int = 1) -> List[Dict[str, str]]:
    """Search for public Spotify playlists based on a list of names."""
    playlists = []

    for name in names:
        if not name:
            logging.warning("Empty playlist name provided. Skipping.")
            continue

        for attempt in range(retries):
            try:
                logging.info(f"Searching Spotify for playlist: {name}")
                result = sp.search(q=name, type='playlist', limit=1)
                items = result.get('playlists', {}).get('items', [])

                if items:
                    playlist = items[0]
                    playlists.append({
                        "name": playlist['name'],
                        "external_urls": playlist['external_urls']
                    })
                else:
                    logging.info(f"No playlist found for: {name}")
                break  # Stop retrying if successful

            except spotipy.exceptions.SpotifyException as e:
                msg = str(e).lower()
                if 'rate limit' in msg:
                    wait_time = delay * (2 ** attempt)
                    logging.warning(f"Rate limit hit while searching playlist '{name}'. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logging.error(f"Spotify API error while searching playlist '{name}': {e}", exc_info=True)
                    break
            except Exception as e:
                logging.error(f"Unexpected error while searching for playlist '{name}': {e}", exc_info=True)
                break

    return playlists
