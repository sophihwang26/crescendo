from flask import Flask, render_template, request
from forms import MusicSearchForm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask_sqlalchemy import SQLAlchemy
import requests
import random


client_id = "99b4bc438bd34e57a55674a469249810"
client_secret = "e3f928cb542849e99a2c65d0db1f8708"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

app = Flask(__name__)

db = SQLAlchemy(app)

class RecentModel(db.Model):
    id = db.Column(db.String(120), unique=False, nullable=True)
    track = db.Column(db.String(120), primary_key=True)
    audio = db.Column(db.String(120), unique=False, nullable=True)
    cover_art = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<Song %r>' % self.track

class TopTracksModel(db.Model):
    id = db.Column(db.String(120), unique=False, nullable=True)
    track = db.Column(db.String(120), primary_key=True)
    audio = db.Column(db.String(120), unique=False, nullable=True)
    cover_art = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<Song %r>' % self.track

db.create_all()
db.session.commit()
AUTH_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID="99b4bc438bd34e57a55674a469249810"
CLIENT_SECRET="e3f928cb542849e99a2c65d0db1f8708"


@app.route('/', methods=['GET', 'POST'])
def index():
    access_token = reset_token()
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    if request.method == 'POST':
        RecentModel.query.delete()
        category_url = f"{request.form['category']}/playlists"
        print(category_url)
        response = requests.get(category_url, headers=headers)
        playlist_id = response.json()['playlists']['items'][random.randrange(0, len(response.json()['playlists']['items']))]['id']
        getplaylist_url = "https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks"
        response = requests.get(getplaylist_url, headers=headers, params={"limit": 30})
        print(response)
        for track in response.json()['items'][:10]:
            t = track['track']['name']
            audio = track['track']['preview_url']
            cover_art = track['track']['album']['images'][0]['url']
            idd = track['track']['album']['artists'][0]['name']
            addRecentModel(idd, t, audio, cover_art)
        for track in response.json()['items'][10:20]:
            t = track['track']['name']
            audio = track['track']['preview_url']
            cover_art = track['track']['album']['images'][0]['url']
            idd = track['track']['album']['artists'][0]['name']
            addTopTrackModel(idd, t, audio, cover_art)
    recent_models = RecentModel.query.all()
    track_models = TopTracksModel.query.all()
    return render_template('index.html', recent_models=recent_models, tracks_models=track_models, categories=categories(headers))

def addRecentModel(id, track, audio, cover_art):
    db.session.add(RecentModel(id=id, track=track, audio=audio, cover_art=cover_art))

def addTopTrackModel(id, track, audio, cover_art):
    db.session.add(TopTracksModel(id=id, track=track, audio=audio, cover_art=cover_art))

def reset_token():
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

def categories(headers):
    response = requests.get("https://api.spotify.com/v1/browse/categories", headers=headers)
    return [(i['name'], i['href']) for i in response.json()['categories']['items']]

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

@app.route('/requests')
def requests_def():
    return render_template('listener/requests.html')

@app.route('/community')
def community():
    return render_template('listener/community.html')

@app.route('/playlists')
def playlists():
    return render_template('listener/playlists.html')

@app.route('/songs')
def songs():
    return render_template('listener/songs.html')

@app.route('/artists')
def artists():
    return render_template('listener/artists.html')

@app.route('/manageRequests')
def manageRequests():
    return render_template('creator/manageRequests.html')

@app.route('/manageCommunity')
def manageCommunity():
    return render_template('creator/manageCommunity.html')

@app.route('/stat')
def stat():
    return render_template('creator/stat.html')

@app.route('/yourMusic')
def yourMusic():
    return render_template('creator/yourMusic.html')

def search_results(search_form):
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
    results = spotify.artist_top_tracks(lz_uri)
    item = results['tracks'][1]
    return {'track': item['name'], 'audio': [item['preview_url']]}

if __name__ == '__main__':
    app.run()
