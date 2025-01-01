# Import required libraries
import os
import google.generativeai as genai
import logging

# Setup for logging configuration
logging.basicConfig(level=logging.DEBUG)

# Load the API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def refine_search_query(keyword):
    try:
        # Request Gemini API to refine the query
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(f"Give me some songs based on the word: {keyword}")
        
        # Get the refined query and log it
        refined_query = response.text.strip() if hasattr(response, 'text') else keyword
        logging.debug(f"Refined search query: {refined_query}")
        
        return refined_query
    except Exception as e:
        logging.error(f"Error from Gemini API: {e}")
        raise Exception(f"Error from Gemini API: {e}")
