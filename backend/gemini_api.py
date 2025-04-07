# Import required libraries
import os
import google.generativeai as genai
import logging
from typing import List

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define values for model and API key
MODEL_NAME = 'gemini-2.0-flash'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini API client
if not GEMINI_API_KEY:
    logging.critical("Missing Gemini API Key. Ensure it is set in environment variables.")
    raise ValueError("Missing Gemini API Key")

genai.configure(api_key=GEMINI_API_KEY)
logging.info("Gemini API successfully configured.")


def get_songs_from_gemini(keyword, max_songs=5):
    """Fetch song suggestions from Gemini API based on a search keyword."""
    # Add input validation
    if not keyword or not isinstance(keyword, str):
        logging.warning("Invalid keyword provided for Gemini API search.")
        return []

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Give me the title of {max_songs} common songs that exist on Spotify in the format Song - Artist related to the word: {keyword}, with no other text than this"

        # Improve error handling
        try:
            response = model.generate_content(prompt)
        except Exception as e:
            logging.error(f"Gemini API error: {e}", exc_info=True)
            return []

        # Parse and clean response
        songs = response.text.strip().split('\n')
        cleaned_songs = [song.strip() for song in songs if '-' in song]

        if not cleaned_songs:
            logging.warning(f"No songs found for keyword: {keyword}")

        logging.info(f"Gemini Suggestions: {cleaned_songs}")
        return cleaned_songs
    except Exception as e:
        logging.error(
            f"Error processing Gemini API response: {e}", exc_info=True)
        return []


def suggest_playlist_names(vibe: str, max_names: int = 5) -> List[str]:
    """Generate playlist name suggestions using the Gemini API based on a vibe input."""
    # Add input validation
    if not vibe or not isinstance(vibe, str):
        logging.warning(
            "Invalid vibe provided for Gemini API playlist name generation.")
        return []

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Generate {max_names} creative names for playlists based on the theme '{vibe}'. Only return a list of names, no extra text."

        try:
            response = model.generate_content(prompt)
        except Exception as e:
            return []

        playlists = response.text.strip().split('\n')
        cleaned_playlists = [name.strip() for name in playlists if name]
        return cleaned_playlists
    except Exception as e:
        return []
