import os
import requests
import json
from flask import Flask, jsonify
from flask_cors import CORS  # Required for your app to access this online
from bs4 import BeautifulSoup

# 1. Initialize the Flask application
app = Flask(__name__)

# 2. Enable CORS so your frontend (React, Flutter, etc.) can talk to this backend
CORS(app)

# 3. Define the scraping logic in a reusable function
def get_jiosaavn_data(url):
    # Spoof a browser header to avoid being blocked by JioSaavn's security
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise error if page fails to load
        
        soup = BeautifulSoup(response.text, 'html.parser')
        songs = []

        # Find all song containers (using JioSaavn's common list class)
        track_items = soup.find_all('div', class_='c-drag')

        for item in track_items:
            # Extract Song Name
            name_tag = item.find('a', class_='u-color-js-gray')
            # Extract Artist Name
            artist_tag = item.find('p', class_='u-centi')

            if name_tag:
                songs.append({
                    "name": name_tag.text.strip(),
                    "artist": artist_tag.text.strip() if artist_tag else "Various Artists"
                })
        
        return songs
    except Exception as e:
        return {"error": f"Failed to scrape data: {str(e)}"}

# 4. Route for Trending Songs in India
@app.route('/api/trending', methods=['GET'])
def trending():
    url = "https://www.jiosaavn.com/featured/trending-songs-india-2026/vzl8nRvFrE5NXRw7JlcL4A__"
    result = get_jiosaavn_data(url)
    return jsonify(result)

# 5. Route for New Releases
@app.route('/api/new-releases', methods=['GET'])
def new_releases():
    url = "https://www.jiosaavn.com/new-releases/hindi"
    result = get_jiosaavn_data(url)
    return jsonify(result)

@app.route('/api/vintage', methods=['GET'])
def new_releases():
    url = "https://www.jiosaavn.com/featured/best-of-retro/IFTYFbu2anRuOxiEGmm6lQ__"
    result = get_jiosaavn_data(url)
    return jsonify(result)

# 6. Default route to check if server is live
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Server is Online", "message": "Use /api/trending or /api/new-releases"})

# 7. Run the app (Production-ready port handling)
if __name__ == '__main__':
    # Cloud hosts like Render/Heroku provide the PORT via environment variables
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
