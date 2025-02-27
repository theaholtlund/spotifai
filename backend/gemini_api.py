# Import required libraries
import os
import google.generativeai as genai
import logging

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define values for model and API key
MODEL_NAME = 'gemini-1.5-pro'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini API client
if not GEMINI_API_KEY:
    logging.critical("Missing Gemini API Key. Ensure it is set in environment variables.")
    raise ValueError("Missing Gemini API Key")

genai.configure(api_key=GEMINI_API_KEY)
logging.info("Gemini API successfully configured.")

def get_songs_from_gemini(keyword, max_songs=5):
    """Fetch song suggestions from Gemini API based on a search keyword."""
    if not keyword:
        logging.warning("No keyword provided for Gemini API search.")
        return []

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Give me the title of {max_songs} common songs that exist on Spotify in the format **Song** - Artist related to the word: {keyword}, with no other text than this"
        response = model.generate_content(prompt)

        # Parse and clean response
        songs = response.text.strip().split('\n')
        cleaned_songs = [song.strip() for song in songs if '-' in song]

        if not cleaned_songs:
            logging.warning(f"No songs found for keyword: {keyword}")

        logging.info(f"Gemini Suggestions: {cleaned_songs}")
        return cleaned_songs
    except Exception as e:
        logging.error(f"Gemini API error: {e}", exc_info=True)
        return []