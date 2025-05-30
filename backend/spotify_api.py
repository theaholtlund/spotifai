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
    logging.info("Spotify client authenticated.")
except Exception:
    logging.critical("Failed to authenticate Spotify API", exc_info=True)
    raise


def search_spotify_tracks(song_name: str, retries: int = 3, delay: int = 1) -> List[Dict]:
    """Search for tracks on Spotify based on query input of title and artist."""
    # Check if the song_name format is valid, must contain a ' - '
    if ' - ' not in song_name:
        logging.warning(f"Invalid song name format: {song_name}")
        return []

    title, artist = map(str.strip, song_name.split(' - ', 1))
    query = f"track:{title} artist:{artist}"

    for attempt in range(retries):
        try:
            logging.info(f"Searching Spotify for: {song_name}")
            result = sp.search(q=query, type='track', limit=1)
            return result.get('tracks', {}).get('items', [])
        except spotipy.exceptions.SpotifyException as e:
            # Handle rate limit exceptions and retry if necessary
            if 'rate limit exceeded' in str(e).lower():
                wait_time = delay * (2 ** attempt)
                logging.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time) # Wait before retrying and retry with increased delay
            else:
                logging.error(f"Spotify API error: {e}", exc_info=True)
                break
        except Exception as e:
            logging.error(f"Unexpected error: {e}", exc_info=True)
            break

    return []


def search_public_playlists_by_name(names: List[str], retries: int = 3, delay: int = 1) -> List[Dict[str, str]]:
    """Search for public Spotify playlists based on a list of names."""
    playlists = []

    for name in names:
        try:
            logging.info(f"Searching for playlist: {name}")
            # Perform the search query on Spotify for each playlist name
            results = sp.search(q=name, type='playlist', limit=1)
            logging.info(f"These are the results for {name}: {results}.")

            # Check if the search results contain valid playlist data
            if results and 'playlists' in results and 'items' in results['playlists']:
                items = results['playlists']['items']
                logging.info(f"These are the items for {name}: {items}.")

                # If valid playlists are found, append the first one to the list
                if items and items != [None]:
                    playlist = items[0]
                    playlists.append({
                        "name": playlist['name'],
                        "external_urls": playlist['external_urls']
                    })
                else:
                    logging.warning(f"No playlists found for: {name}")
            else:
                logging.warning(
                    f"Empty or invalid results returned for: {name}")

            except spotipy.exceptions.SpotifyException as e:
                # Handle rate limit exceptions and retry if necessary
                if 'rate limit exceeded' in str(e).lower():
                    wait_time = delay * (2 ** attempt)
                    logging.warning(f"Rate limited. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logging.error(f"Spotify API error: {e}", exc_info=True)
                    break
            except Exception as e:
                logging.error(f"Unexpected error searching for playlist '{name}': {e}", exc_info=True)
                break

    return playlists
