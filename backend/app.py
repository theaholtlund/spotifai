# Import required libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from spotify_api import search_tracks
from gemini_api import get_songs_from_gemini
import logging

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialise Flask app
app = Flask(__name__)
CORS(app)

def error_response(message, status_code):
    """Utility function to return standardised error responses."""
    logging.error(f"Error {status_code}: {message}")
    return jsonify({"error": message}), status_code

@app.route('/search', methods=['POST'])
def search_songs_with_gemini_suggestions():
    """Endpoing to search for songs and fetch Gemini suggestions."""
    try:
        data = request.get_json()

        # Validate request payload
        if not data or 'query' not in data:
            return error_response("Query is required", 400)

        query = data['query'].strip()
        logging.info(f"Received query: {query}")

        if not query:
            return error_response("Query cannot be empty", 400)

        # Fetch song suggestions from Gemini
        gemini_songs = get_songs_from_gemini(query)
        if not gemini_songs:
            return error_response("No song suggestions found", 404)

        # Search for tracks on Spotify based on Gemini suggestions
        tracks_found, tracks_not_found = [], []
        for song in gemini_songs:
            spotify_results = search_tracks(song)
            if spotify_results:
                tracks_found.extend(spotify_results)
            else:
                tracks_not_found.append(song)

        top_5_tracks = tracks_found[:5] if tracks_found else []

        logging.info(f"Tracks not found on Spotify: {tracks_not_found}")
        return jsonify({"tracks": top_5_tracks, "not_found": tracks_not_found})

    except Exception as e:
        logging.exception("Unexpected server error")
        return error_response("Internal server error", 500)

if __name__ == '__main__':
    app.run(debug=True)