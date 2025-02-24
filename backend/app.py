# Import required libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from spotify_api import search_tracks
from gemini_api import get_songs_from_gemini
import logging
import traceback

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialise Flask app
app = Flask(__name__)
CORS(app)

def error_response(message, status_code):
    """Utility function to return standardised error responses."""
    logging.error(f"Error {status_code}: {message}")
    return jsonify({"error": message}), status_code

def find_spotify_tracks(song_list):
    """Search for tracks on Spotify based on a list of song names, return tracks found and tracks not found."""
    if not song_list:
        return [], []  # Return empty lists if no songs are provided

    tracks_found = []
    tracks_not_found = []

    for song in song_list:
        try:
            spotify_results = search_tracks(song)
            if spotify_results:
                tracks_found.extend(spotify_results)
            else:
                tracks_not_found.append(song)
        except Exception as e:
            logging.error(f"Error searching for track '{song}' on Spotify: {str(e)}")
            tracks_not_found.append(song)

    return tracks_found, tracks_not_found

@app.route('/search', methods=['POST'])
def search_songs_with_gemini_suggestions():
    """Endpoint to search for songs and fetch Gemini suggestions."""
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
        try:
            gemini_songs = get_songs_from_gemini(query)
        except Exception as e:
            logging.error(f"Error fetching songs from Gemini: {str(e)}\n{traceback.format_exc()}")
            return error_response("Failed to fetch songs from Gemini", 500)

        if not gemini_songs:
            logging.info("No song suggestions found")
            return error_response("No song suggestions found", 404)

        # Search for tracks on Spotify based on Gemini suggestions
        tracks_found, tracks_not_found = find_spotify_tracks(gemini_songs)

        logging.info(f"Tracks found: {len(tracks_found)}, tracks not found: {len(tracks_not_found)}")

        return jsonify({
            "tracks": tracks_found[:5] if tracks_found else [],
            "not_found": tracks_not_found
        })

    except Exception as e:
        logging.exception(f"Unexpected server error: {e}")
        return error_response(f"Internal server error: {str(e)}", 500)

if __name__ == '__main__':
    app.run(debug=True)
