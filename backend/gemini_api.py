# Import required libraries
import os
import google.generativeai as genai

# Load the API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def generate_playlist_description(prompt):
    """
    Generate a playlist description using Google Gemini API.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(f"Generate a playlist description for: {prompt}")
        
        # Extract and return the response text
        return response.text.strip() if hasattr(response, 'text') else "No description generated."
    except Exception as e:
        raise Exception(f"Error from Gemini API: {e}")
