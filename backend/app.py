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
