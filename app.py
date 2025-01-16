from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_CLIENT_ID = "81b8fe84e01b41a3931baa0c206f5846"
SPOTIFY_CLIENT_SECRET = "3820b750717a41b38a0f46043095a23c"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_playlist', methods=['POST'])
def get_playlist():
    mood = request.form['mood']
    mood_sentiment = get_mood_sentiment(mood)
    playlist = generate_playlist(mood_sentiment)
    return jsonify(playlist)

def get_mood_sentiment(mood_text):
    blob = TextBlob(mood_text)
    sentiment = blob.sentiment.polarity  

    if sentiment > 0.1:
        return 'happy'
    elif sentiment < -0.1:
        return 'sad'
    else:
        return 'neutral'

def generate_playlist(mood):
    if mood == 'happy':
        genre = 'pop'
    elif mood == 'sad':
        genre = 'Coffeehouse'
    else:
        genre = 'classical'

    try:
    
        result = sp.search(q=f"{genre} playlist", type="playlist", limit=20)

        print("Spotify API response:", result)

  
        if not result or 'playlists' not in result or not result['playlists'].get('items'):
            print("No playlists found or invalid API response format.")
            return {'playlists': ['https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M']}  
        
        playlists = result['playlists']['items']
        playlist_urls = [playlist['external_urls']['spotify'] for playlist in playlists if 'external_urls' in playlist]
        
        if not playlist_urls:
            print("No valid playlists URLs found.")
            return {'playlists': ['https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M']}  

        return {'playlists': playlist_urls}

    except Exception as e:
        
        print(f"Error while generating playlist: {e}")
        return {'playlists': ['https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M']}


if __name__ == '__main__':
    app.run(debug=True)
