# Import required libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from spotify_api import search_tracks
from gemini_api import get_songs_from_gemini
import logging

# Setup for logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the Flask instance
app = Flask(__name__)
CORS(app)

def error_response(message, status_code):
    """Utility function to create standardised error responses."""
    logging.error(f"Error {status_code}: {message}")
    return jsonify({"error": message}), status_code

@app.route('/search', methods=['POST'])
def search_songs_with_gemini_suggestions():
    try:
        data = request.get_json()

        # Validate request payload
        if not data or 'query' not in data:
            return error_response("Query is required", 400)

        query = data['query'].strip()

        if not query:
            return error_response("Query cannot be empty", 400)

        # Get song suggestions from Gemini API
        gemini_songs = get_songs_from_gemini(query)

        if not gemini_songs:
            return error_response("No song suggestions found", 404)

        # Search for tracks on Spotify based on Gemini suggestions
        all_tracks = [track for song in gemini_songs for track in search_tracks(song)]
        top_5_tracks = all_tracks[:5] if all_tracks else []

        logging.info(f"Top 5 Songs found on Spotify: {[track['name'] for track in top_5_tracks]}")
        return jsonify({"tracks": top_5_tracks})

    except Exception as e:
        return error_response("Internal server error", 500)

if __name__ == '__main__':
    app.run(debug=True)
