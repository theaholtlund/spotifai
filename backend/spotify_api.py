# Import required libraries
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"), 
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

def search_tracks(query):
    # Sanitize the query and limit characters
    sanitized_query = query.split('\n')[0].split(':')[0]
    sanitized_query = sanitized_query[:250]
    
    results = sp.search(q=sanitized_query, type='track', limit=5)
    return results['tracks']['items']
