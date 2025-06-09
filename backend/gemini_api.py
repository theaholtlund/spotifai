# Import required libraries
import os
import logging
from typing import List
import google.generativeai as genai

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define values for model and API key
MODEL_NAME = 'gemini-2.0-flash'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


def configure_gemini():
    """Configure the Gemini API client."""
    if not GEMINI_API_KEY:
        logging.critical("Missing Gemini API key. Ensure it is set in the environment variables.")
        raise ValueError("Missing Gemini API key.")
    
    genai.configure(api_key=GEMINI_API_KEY)
    logging.info("Gemini API successfully configured.")


# Configure the Gemini API client
configure_gemini()


def get_songs_from_gemini(keyword, max_songs=5) -> List[str]:
    """Fetch song suggestions from Gemini API based on a search keyword."""
    if not isinstance(keyword, str) or not keyword.strip():
        logging.warning("Invalid keyword for Gemini API search.")
        return []

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = (
            f"Give me the title of {max_songs} common songs that exist on Spotify in the format "
            f"Song - Artist related to the word: {keyword}, with no other text than this"
        )

        # Parse and clean response
        response = model.generate_content(prompt)
        songs = response.text.strip().split('\n')
        cleaned_songs = [song.strip() for song in songs if '-' in song]

        if not cleaned_songs:
            logging.warning(f"No songs found for keyword: {keyword}")

        logging.info(f"Gemini suggestions: {cleaned_songs}")
        return cleaned_songs

    except Exception as e:
        logging.error(f"Gemini API error while fetching songs: {e}", exc_info=True)
        return []


def suggest_playlist_names(vibe: str, max_names: int = 5) -> List[str]:
    """Generate playlist name suggestions using the Gemini API based on a vibe input."""
    if not isinstance(vibe, str) or not vibe.strip():
        logging.warning("Invalid vibe for Gemini API playlist name generation.")
        return []

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = (
            f"Generate {max_names} creative names for playlists based on the theme '{vibe}'. "
            f"Only return a list of names, no extra text."
        )

        try:
            response = model.generate_content(prompt)
        except Exception as e:
            logging.error(f"Gemini API error: {e}", exc_info=True)
            return []

        # Parse and clean response
        playlists = response.text.strip().split('\n')
        cleaned_playlists = [name.strip() for name in playlists if name]

        if not cleaned_playlists:
            logging.warning(f"No playlist names found for vibe: {vibe}")

        logging.info(f"Gemini Playlist Name Suggestions: {cleaned_playlists}")
        return cleaned_playlists

    except Exception as e:
        logging.error(f"Gemini API error while generating playlist names: {e}", exc_info=True)
        return []
