#/usr/bin/env python

## Add files to playlist via POST to /add:
## curl -i -H "Content-Type: application/json" -X POST -d '{"path":"/edia/music/Misc/The Champs - Tequila.mp3"}' http://localhost:5000/add

from flask import Flask, render_template, request
app = Flask(__name__)

import jukebox
import os
import json
from pprint import pprint as pp

JUKE = jukebox.Jukebox()

@app.route('/')
def top():
    return "MISHAP JukeBox!"

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    JUKE.start_jukebox()
    return "Jukebox Started!"

@app.route('/get/list')
def get_playlist():
    return json.dumps(JUKE.playlist)

@app.route('/get/songs')
def get_songlist():
    songs = JUKE.songlist.list_all_songs_by_artist()
    retval = {a:[{'artist':s.artist,'title':s.title} for s in songs[a]] for a in songs.keys()}
    return json.dumps(retval)

@app.route('/add', methods = ['POST'])
def add():
    # 'path' should be used only for testing.
    # For production, we probably don't want to allow
    # someone to send a filesys path!
    if not request.json or not 'path' in request.json:
        abort(400)
    songpath = request.json.get('path',None)
    if os.path.isfile(songpath):
        JUKE.playlist.append(songpath)
    else:
        return "%s file does not exist."%songpath
    print "Added %s"%songpath
    print "Starting Jukebox"
    JUKE.start_jukebox()
    return "added",songpath

if __name__ == '__main__':
    import sys
    if 'debug' in sys.argv:
        print "Flask DEBUG"
        app.run(debug = True)
    else:
        print "Flask Production"
        app.run(host='0.0.0.0')
