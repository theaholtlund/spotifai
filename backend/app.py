# Import required libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from spotify_api import search_tracks

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' parameter in request body"}), 400

    query = data['query']
    tracks = search_tracks(query)
    
    formatted_tracks = []
    for item in tracks:
        formatted_tracks.append({
            'name': item['name'],
            'artists': [{'name': artist['name']} for artist in item['artists']],
            'album': {
                'images': item['album'].get('images', [])
            },
            'external_urls': {
                'spotify': item['external_urls'].get('spotify', '')
            }
        })
    return jsonify({'tracks': formatted_tracks})


if __name__ == '__main__':
    app.run(debug=True)
