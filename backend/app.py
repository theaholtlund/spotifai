# Import required libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from spotify_api import search_tracks
from gemini_api import get_songs_from_gemini
import logging

# Setup for logging configuration
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search_tracks_with_refinement():
    data = request.get_json()

    # Check if the query is present in the request
    if not data or 'query' not in data:
        return jsonify({"error": "Query is required"}), 400

    query = data['query'].strip()

 

    # Get song suggestions from Gemini API
    gemini_songs = get_songs_from_gemini(query)

    # If no songs are returned by Gemini, return an error
    if not gemini_songs:
        return jsonify({"error": "No song suggestions found"}), 404

    # Extract the relevant song titles and artist names from Gemini suggestions
    song_artist_pairs = extract_song_and_artist(gemini_songs)
    print("Song artist bla bla: ", song_artist_pairs)

    # Search Spotify using the refined query
    tracks = search_tracks(refined_query)

    # Log the refined query and the tracks that will be returned
    logging.debug(f"Refined query used for Spotify search: {refined_query}")
    
    return jsonify({"tracks": tracks})

if __name__ == '__main__':
    app.run(debug=True)
