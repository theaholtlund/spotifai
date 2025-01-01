# Import required libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from spotify_api import search_tracks
from gemini_api import refine_search_query
import logging

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search_tracks_with_refinement():
    data = request.get_json()

    # Check if the query is present in the request
    if not data or 'query' not in data:
        return jsonify({"error": "Query is required"}), 400

    query = data['query'].strip()

    logging.debug(f"Received query from frontend: {query}")

    # Refine the query using the Gemini API
    refined_query = refine_search_query(query)

    # Search Spotify using the refined query
    tracks = search_tracks(refined_query)

    # Log the refined query and the tracks that will be returned
    logging.debug(f"Refined query used for Spotify search: {refined_query}")
    
    return jsonify({"tracks": tracks})

if __name__ == '__main__':
    app.run(debug=True)
