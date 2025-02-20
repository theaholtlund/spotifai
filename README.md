### Spotifai

## 🚀 Overview

This project (tentatively) uses Google Gemini API to suggest songs based on a theme and Spotify API to display those songs in the browser.

## 🛠️ Setup

1. Clone this repository.
2. Create a virtual environment: `python -m venv venv`.
3. Install dependencies: `pip install -r backend/requirements.txt`.
4. Add API keys to `.env`.

## 🔑 API Keys Required

- Gemini API Key, created and located [here](https://aistudio.google.com/app/apikey).
- Spotify Client ID & Secret, created and located [here](https://developer.spotify.com/dashboard).

## 🎵 How it Works

1. Enter a mood or theme in the frontend UI.
2. Gemini API generates the song suggestions.
3. Spotify displays the songs that have been suggested.

## 📝 Run the Project

1. Activate the venv (Mac/Linux):

```bash
source venv/bin/activate
```

2. Run the backend:

```bash
python backend/app.py
```

3. Open frontend/index.html in your browser.

```bash
open -a "Google Chrome" frontend/index.html
```
