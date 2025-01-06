# Import required libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from spotify_api import search_tracks
from gemini_api import get_songs_from_gemini
import logging

# Setup for logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

# Utility error handler
def error_response(message, status_code):
    return jsonify({"error": message}), status_code

@app.route('/search', methods=['POST'])
def search_songs_with_gemini_suggestions():
    data = request.get_json()

    # Check if the query is present in the request
    if not data or 'query' not in data:
        return error_response("Query is required", 400)

    query = data['query'].strip()

    # Get song suggestions from Gemini API
    gemini_songs = get_songs_from_gemini(query)

    # If no songs are returned by Gemini, return an error
    if not gemini_songs:
        return jsonify({"error": "No song suggestions found"}), 404

    all_tracks = [track for song in gemini_songs for track in search_tracks(song)]
    top_5_tracks = all_tracks[:5]

    logging.info(f"Songs found on Spotify: {[track['name'] for track in top_5_tracks]}")

    return jsonify({"tracks": top_5_tracks})

def extract_song_and_artist(gemini_songs):
    song_artist_pairs = []
    
    for song in gemini_songs:
        # Each song is already in the format "Song Title by Artist"
        if ' by ' in song:
            try:
                song_artist_pairs.append(song.strip())
            except IndexError:
                logging.warning(f"Skipping invalid song format: {song}")
        else:
            logging.warning(f"Skipping invalid song format: {song}")

    return song_artist_pairs

if __name__ == '__main__':
    app.run(debug=True)
