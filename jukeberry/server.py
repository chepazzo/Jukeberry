#/usr/bin/env python

## Add files to playlist via POST to /add:
## curl -i -H "Content-Type: application/json" -X POST -d '{"path":"/edia/music/Misc/The Champs - Tequila.mp3"}' http://localhost:5000/add

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import jukebox
import os
import json
from pprint import pprint as pp

JUKE = jukebox.Jukebox()

## Pages

@app.route('/')
def top():
    return render_template('index.html',
        list=list,
    #    json=json,
    #    currsong=JUKE.currsong,
    #    songlist=sorted(JUKE.songlist.list_all_songs_by_artist(),key=lambda x: x.title),
    #    playlist=JUKE.playlist
    )

@app.route('/JukeCtrl.js')
def jukectrljs():
    return render_template('JukeCtrl.js')

@app.route('/artists.html')
def artists():
    return render_template('artists.html')#,
    #    artists=sorted(JUKE.songlist.list_artists())
    #)

@app.route('/<string:artist>/songs.html')
def songs(artist):
    #artist = request.args.get('artist')
    return render_template('songs.html',
    #    json=json,
    #    songs=JUKE.songlist.get_songs_by_artist(artist),
        artist=artist
    )

## API

@app.route('/loadcatalog')
def load_catalog():
    JUKE.load_catalog()
    retval = [s._serialize() for s in JUKE.playlist]
    return jsonify(succ(value=retval))

@app.route('/get/artists')
def get_artists():
    retval=sorted(JUKE.songlist.list_artists())
    return jsonify(succ(value=retval))

@app.route('/get/playlist')
def get_playlist():
    retval = [s._serialize() for s in JUKE.playlist]
    return jsonify(succ(value=retval))

@app.route('/get/songlist')
def get_songlist():
    songs = JUKE.songlist.list_all_songs_by_artist()
    retval = {a:[s._serialize() for s in songs[a]] for a in songs.keys()}
    #retval = {a:[s._serialize(skip=['filename']) for s in songs[a]] for a in songs.keys()}
    return jsonify(succ(value=retval))

@app.route('/get/currsong')
def get_currsong():
    retval = JUKE.currsong._serialize()
    #retval = {a:[s._serialize(skip=['filename']) for s in songs[a]] for a in songs.keys()}
    return jsonify(succ(value=retval))

@app.route('/add', methods = ['POST'])
def add():
    # 'path' should be used only for testing.
    # For production, we probably don't want to allow
    # someone to send a filesys path!
    #if not request.json or not 'path' in request.json:
    #    abort(400)
    #songpath = request.json.get('path',None)
    pp(request.json)
    songs = JUKE.songlist.get_songs_by_keyword(**request.json)
    pp([s._serialize() for s in songs])
    for song in songs:
        songpath = song.filename
        if os.path.isfile(songpath):
            JUKE.playlist.append(song)
            #JUKE.playlist.append(songpath)
        else:
            return jsonify(fail("%s file does not exist."%songpath))
        print "Added %s"%songpath
        print "Starting Jukebox"
    JUKE.start_jukebox()
    song_titles = [s.title for s in songs]
    return jsonify(succ(value=song_titles))

## Start/Stop
@app.route('/start')
def start():
    JUKE.start_jukebox()
    return "Jukebox Started!"

def succ(field='data',value=''):
    ''' {'stat':'ok', 'data':{} '''
    return {'stat':'ok',field:value}

def fail(msg='',code=0):
    ''' {'stat':'fail', 'err':{'msg':'', 'code':0}} '''
    err = {'msg':msg,'code':code}
    return {'stat':'fail','err':err}

def main():
    import sys
    if 'debug' in sys.argv:
        print "Flask DEBUG"
        app.run(debug = True)
    else:
        print "Flask Production"
        app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
