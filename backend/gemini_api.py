# Import required libraries
import os
import google.generativeai as genai
import logging

# Setup for logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set values for model and API key
MODEL_NAME = 'gemini-1.5-pro'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini API client
try:
    if not GEMINI_API_KEY:
        raise ValueError("Missing Gemini API Key")
    genai.configure(api_key=GEMINI_API_KEY)
    logging.info("Gemini API client successfully configured.")
except Exception as e:
    logging.critical("Failed to configure Gemini API client.", exc_info=True)
    raise e

def get_songs_from_gemini(keyword):
    """Fetch song suggestions from the Gemini API based on search keyword."""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(f"Give me the title of 5 common songs that exist on Spotify in the format **Song** - Artist related to the word: {keyword}, with no other text than this")

        # Parse and clean response
        songs = response.text.strip().split('\n')

        cleaned_songs = [
            f"{song.split('**')[1].strip()} by {song.split('-')[1].strip()}"
            for song in songs if '**' in song and '-' in song
        ]
        logging.info(f"Song suggestions from Gemini: {cleaned_songs}")
        return cleaned_songs
    except Exception as e:
        logging.error(f"Gemini API error: {e}", exc_info=True)
        return []