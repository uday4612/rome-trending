from flask import Flask, jsonify
from flask_cors import CORS  # <-- Add this
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app) # <-- This allows your app to "talk" to this server online

def scrape_data():
    # ... your existing BeautifulSoup logic here ...
    return [{"name": "Song 1", "artist": "Artist 1"}]

@app.route('/trending')
def trending():
    songs = scrape_data()
    return jsonify(songs)

if __name__ == "__main__":
    # Note: On most cloud hosts, you don't use app.run(). 
    # They use a "Start Command" like: gunicorn app:app
    app.run()
