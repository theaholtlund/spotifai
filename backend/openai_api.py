# Import required libraries
import os
from openai import OpenAI
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_playlist_description(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Generate a playlist description for the vibe: {prompt}"}
        ]
    )
    return response['choices'][0]['message']['content'].strip()
