# Import required libraries
import time
import logging
from functools import wraps
from typing import List, Tuple
from cachetools import TTLCache
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from spotify_api import search_spotify_tracks, search_public_playlists_by_name
from gemini_api import get_songs_from_gemini, suggest_playlist_names

# Initialise Flask app
app = Flask(__name__)
CORS(app)

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Caching setup
gemini_cache = TTLCache(maxsize=100, ttl=300)  # 5 minutes cache
spotify_cache = TTLCache(maxsize=100, ttl=300)  # 5 minutes cache

# Rate limiting setup
RATE_LIMIT = 5  # Requests per minute
request_times = []
search_history = []


def rate_limit(func):
    """Decorator to limit the number of API requests per minute."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        now = time.time()
        request_times[:] = [t for t in request_times if t > now - 60]
        if len(request_times) >= RATE_LIMIT:
            return jsonify({"error": "too many requests, please try again later."}), 429
        request_times.append(now)
        return func(*args, **kwargs)
    return wrapper


def error_response(message: str, status_code: int):
    """Utility function to return standardised error responses."""
    logging.error(f"{status_code} - {message}")
    return jsonify({"error": message}), status_code


def find_spotify_tracks(song_list: List[str]) -> Tuple[List[dict], List[str]]:
    """Return track data from Spotify and a list of unfound songs."""
    tracks_found = []
    tracks_not_found = []

    for song in song_list:
        try:
            if song in spotify_cache:
                results = spotify_cache[song]
            else:
                results = search_spotify_tracks(song)
                spotify_cache[song] = results

            if results:
                tracks_found.extend(results)
            else:
                tracks_not_found.append(song)
        except Exception as e:
            logging.exception(f"Error searching for track: '{song}'")
            tracks_not_found.append(song)

    return tracks_found, tracks_not_found


@app.route('/search', methods=['POST'])
@rate_limit
def search_songs_with_gemini_suggestions():
    """Endpoint to search for songs and fetch Gemini suggestions."""
    try:
        data = request.get_json()
        query = (data or {}).get('query', '').strip()

        logging.info(f"Received query: {query}")

        if not query:
            return error_response("Query is required and cannot be empty", 400)

        logging.info(f"Received query: {query}")

        gemini_songs = gemini_cache.get(query) or get_songs_from_gemini(query)
        gemini_cache[query] = gemini_songs

        if not gemini_songs:
            return error_response("No song suggestions found", 404)

        tracks_found, tracks_not_found = find_spotify_tracks(gemini_songs)

        logging.info(f"Tracks found: {len(tracks_found)}, Not found: {len(tracks_not_found)}")
        search_history.append({
            "query": query,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "tracks_found": [t['name'] for t in tracks_found],
            "not_found": tracks_not_found
        })

        return jsonify({
            "tracks_found": tracks_found,
            "tracks_not_found": tracks_not_found
        }), 200

    except Exception as e:
        logging.exception("Unexpected error during song search")
        return error_response(f"Internal server error: {str(e)}", 500)


@app.route('/suggest_playlists', methods=['GET'])
def suggest_playlists():
    try:
        vibe = request.args.get('vibe', '').strip()
        if not vibe:
            return error_response("Vibe is required", 400)

        suggested_names = suggest_playlist_names(vibe, max_names=5)
        playlists = search_public_playlists_by_name(suggested_names)
        return jsonify({"playlists": playlists}), 200

    except Exception as e:
        logging.exception(f"Unexpected error during playlist suggestion: {e}")
        return error_response(f"Internal server error: {str(e)}", 500)


@app.route('/health', methods=['GET'])
def health_check():
    return make_response(jsonify({'status': 'ok'}), 200)


if __name__ == '__main__':
    app.run(debug=True)
