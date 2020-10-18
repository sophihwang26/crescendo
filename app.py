from flask import Flask, render_template, request
import os
from forms import MusicSearchForm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "99b4bc438bd34e57a55674a469249810"
client_secret = "e3f928cb542849e99a2c65d0db1f8708"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/test')
def test():
    return 'Test Page'

@app.route('/search', methods=['GET', 'POST'])
def search():
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return render_template('search.html', form=search, results=search_results(search)['audio'])
    return render_template('search.html', form=search, results=[])

@app.route('/music')
@app.route('/music/<name>/<song>/<path:url>')
def music(name=None, song=None, url=None):
    print(url)
    return render_template('music.html', name=name, song=song, url=url)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

def search_results(search_form):
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
    results = spotify.artist_top_tracks(lz_uri)
    item = results['tracks'][1]
    return {'track': item['name'], 'audio': [item['preview_url']]}

if __name__ == '__main__':
    app.run()
