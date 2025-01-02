# Import required libraries
import os
import google.generativeai as genai
import logging

# Setup for logging configuration
logging.basicConfig(level=logging.INFO)

# Load the API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def get_songs_from_gemini(keyword):
    try:
        # Ask the Gemini API to provide 5 songs related to the keyword
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(f"Give me the title of 5 songs related to the word: {keyword}")

        # Get the list of songs from the response text
        songs = response.text.strip().split('\n')
        print("Songs:", songs)

        # Clean the songs list to only extract the song title and artist
        cleaned_songs = []
        for song in songs:
            # Each song is in the format 'X. **Song Title** - Artist'
            if '**' in song and '-' in song:
                try:
                    # Extract the song title and artist
                    song_title = song.split('**')[1].strip()  # Extract text between ** **
                    artist_name = song.split('-')[1].strip()  # Extract text after '-'
                    cleaned_songs.append(f"{song_title} by {artist_name}")
                except IndexError:
                    logging.warning(f"Skipping invalid song format: {song}")
            else:
                logging.warning(f"Skipping invalid song format: {song}")
        
        logging.info(f"Song suggestions from Gemini: {cleaned_songs}")

        return cleaned_songs
    except Exception as e:
        logging.error(f"Error from Gemini API: {e}")
        raise Exception(f"Error from Gemini API: {e}")
