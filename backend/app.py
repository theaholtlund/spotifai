# Import required libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from spotify_api import search_tracks

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search_songs():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        tracks = search_tracks(query)
        return jsonify(tracks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
