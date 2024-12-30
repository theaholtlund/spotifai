# Import required libraries
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_playlist_description(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Generate a playlist description for the vibe: {prompt}"}
        ]
    )
    return response['choices'][0]['message']['content'].strip()
