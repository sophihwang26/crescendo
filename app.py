from flask import Flask, render_template, request
import os
from forms import MusicSearchForm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask_sqlalchemy import SQLAlchemy


client_id = "99b4bc438bd34e57a55674a469249810"
client_secret = "e3f928cb542849e99a2c65d0db1f8708"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

app = Flask(__name__)

db = SQLAlchemy(app)

class RecentModel(db.Model):
    id = db.Column(db.String(120), unique=False, nullable=False)
    track = db.Column(db.String(120), primary_key=True)
    audio = db.Column(db.String(120), unique=False, nullable=False)
    cover_art = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Song %r>' % self.track

class TopTracksModel(db.Model):
    id = db.Column(db.String(120), unique=False, nullable=False)
    track = db.Column(db.String(120), primary_key=True)
    audio = db.Column(db.String(120), unique=False, nullable=False)
    cover_art = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Song %r>' % self.track

db.create_all()

s1 = RecentModel(id="Led Zeppelin", track="Stairway to Heaven", audio="https://p.scdn.co/mp3-preview/8226164717312bc411f8635580562d67e191a754?cid=99b4bc438bd34e57a55674a469249810", cover_art="https://i.scdn.co/image/ab67616d0000b273c8a11e48c91a982d086afc69")
s2 = RecentModel(id="Led Zeppelin", track="Whole Lotta Love", audio="https://p.scdn.co/mp3-preview/ce11b19a4d2de9976d7626df0717d0073863909c?cid=99b4bc438bd34e57a55674a469249810", cover_art="https://i.scdn.co/image/ab67616d0000b273fc4f17340773c6c3579fea0d")
s3 = RecentModel(id="Led Zeppelin", track="Immigrant Song", audio="https://p.scdn.co/mp3-preview/8455599677a13017978dcd3f4b210937f0a16bcb?cid=99b4bc438bd34e57a55674a469249810", cover_art="https://i.scdn.co/image/ab67616d0000b27390a50cfe99a4c19ff3cbfbdb")
s4 = RecentModel(id="Led Zeppelin", track="Black Dog", audio="https://p.scdn.co/mp3-preview/9b76619fd9d563a48d38cc90ca00c3008327b52e?cid=99b4bc438bd34e57a55674a469249810", cover_art="https://i.scdn.co/image/ab67616d0000b273c8a11e48c91a982d086afc69")

for i in [s1, s2, s3, s4]:
    db.session.add(i)

db.session.commit()



@app.route('/')
def index():
    models = RecentModel.query.all()
    return render_template('index.html', recent_models=models)

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
def requests():
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
