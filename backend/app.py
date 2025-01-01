# Import required libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_api import generate_playlist_description
from spotify_api import create_playlist, add_tracks_to_playlist, sp

app = Flask(__name__)

# Allow requests from frontend origin
CORS(app, resources={r"/generate": {"origins": "*"}})

@app.route('/generate', methods=['POST'])
def generate_playlist():
    data = request.json
    prompt = data.get('prompt')
    user_id = sp.me()['id']

    description = generate_playlist_description(prompt)
    playlist_id = create_playlist(user_id, "AI Playlist", description)
    add_tracks_to_playlist(playlist_id, ["spotify:track:7GhIk7Il098yCjg4BQjzvb"])

    return jsonify({"message": "Playlist created!", "description": description, "playlist_id": playlist_id})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
