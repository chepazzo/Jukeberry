#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This is the main server module that runs the Flask Server.

Examples:

  Add files to playlist via POST to /add::

    curl -i -H "Content-Type: application/json" -X POST -d '{"path":"/media/music/Misc/The Champs - Tequila.mp3"}' http://localhost:5000/add

'''
import os
import json
from pprint import pprint as pp

try:
    from flask import Flask, render_template, request, jsonify
    app = Flask(__name__)
    FLASK_INSTALLED = True
except:
    FLASK_INSTALLED = False

try:
    import jukebox
    JUKE = jukebox.Jukebox()
    JUKEBOX_INSTALLED = True
except:
    JUKEBOX_INSTALLED = False

## Pages

@app.route('/')
def top():
    '''
    The main route that points to index.html
    '''
    return render_template('index.html',
        list=list,
    )

@app.route('/JukeCtrl.js')
def jukectrljs():
    '''
    AngularJS control javascript.
    '''
    return render_template('JukeCtrl.js')

@app.route('/settings.html')
def settings():
    '''
    The settings view to modify player settings.
    '''
    return render_template('settings.html',
        list=list,
    )

@app.route('/current.html')
def onepage():
    '''
    Former front page.

    ** Need to depricate **
    '''
    return render_template('current.html',
        list=list,
    )

@app.route('/artists.html')
def artists():
    '''
    Former list artists page.

    ** Need to depricate **
    '''
    return render_template('artists.html')#,
    #    artists=sorted(JUKE.songlist.list_artists())
    #)

@app.route('/genres.html')
def genres():
    '''
    Former list genres page.

    ** Need to depricate **
    '''
    return render_template('genres.html')#,

@app.route('/artist/<string:artist>/songs.html')
def songs_by_artist(artist):
    '''
    Former songs by artist page.

    ** Need to depricate **
    '''
    #artist = request.args.get('artist')
    return render_template('songs.html',
    #    json=json,
    #    songs=JUKE.songlist.get_songs_by_artist(artist),
        field='artist',
        value=artist
    )

@app.route('/genre/<string:genre>/songs.html')
def songs_by_genre(genre):
    '''
    Former songs by genrte page.

    ** Need to depricate **
    '''
    return render_template('songs.html',
        field='genre',
        value=genre
    )

## API

@app.route('/loadcatalog')
def load_catalog():
    '''
    Loads catalog from disk.

    Returns:
      json(list): A serialized list of songs currently in the playlist
    '''
    JUKE.load_catalog()
    retval = [s._serialize() for s in JUKE.playlist]
    return jsonify(succ(value=retval))

@app.route('/get/artists')
def get_artists():
    '''
    Get a list of artists.

    Returns:
      json(list): A list of artist names.
    '''
    retval=sorted(JUKE.songlist.list_artists())
    return jsonify(succ(value=retval))

@app.route('/get/playlist')
def get_playlist():
    '''
    Get current playlist.

    Returns:
      json(list): A serialized list of songs currently in the playlist
    '''
    retval = [s._serialize() for s in JUKE.playlist]
    return jsonify(succ(value=retval))

## get_songlist is depricated
@app.route('/get/songlist')
def get_songlist():
    '''
    ** Depricated **

    ** Do Not Use **
    '''
    songs = JUKE.songlist.list_all_songs_by_artist()
    retval = {a:[s._serialize() for s in songs[a]] for a in songs.keys()}
    #retval = {a:[s._serialize(skip=['filename']) for s in songs[a]] for a in songs.keys()}
    return jsonify(succ(value=retval))

@app.route('/get/songs')
def get_songs():
    '''
    Get current playlist.

    Returns:
      json(list): A serialized list of all of the songs.
    '''
    songs = JUKE.songlist
    retval = [s._serialize() for s in songs]
    #retval = {a:[s._serialize(skip=['filename']) for s in songs[a]] for a in songs.keys()}
    return jsonify(succ(value=retval))

@app.route('/get/currsong')
def get_currsong():
    '''
    Get current song.

    Returns:
      json(list): A serialization of the currently playing song.
    '''
    retval = JUKE.currsong;
    if retval is not None:
        retval = retval._serialize()
    #retval = {a:[s._serialize(skip=['filename']) for s in songs[a]] for a in songs.keys()}
    return jsonify(succ(value=retval))

@app.route('/get/alwayson')
def get_alwayson():
    '''
    Get the always_on status.

    Returns:
      json(dict): The current status of always_on.
    '''
    retval = JUKE.alwayson;
    return jsonify(succ(value=retval))

@app.route('/set/alwayson', methods = ['POST'])
def set_alwayson():
    '''
    Set the always_on status.

    Args:
      status (bool): New status to set for always_on.
      filter (dict): Key:value to use to filter the songs randomly chosen when always_on.

        | example: ``{"artist":"Mike Patton"}``
    '''
    content = request.get_json(silent=True)
    if content is None:
        return jsonify(fail(msg="No data sent in request!"))
    if content in [True,False]:
        JUKE.alwayson['status'] = content
    else:
        if 'status' in content.keys():
            JUKE.alwayson['status'] = content['status']
        if 'filters' in content.keys():
            JUKE.alwayson['filters'] = content['filters']
    return jsonify(succ(value=JUKE.alwayson))

@app.route('/add', methods = ['POST'])
def add():
    '''
    Add a song to the current playlist.

    All arguments should be sent as data in a single json object.

    Args:
      content (dict): Request should include, as data, a series of key:value pairs
        corresponding to jukeberry.catalog.Song() attributes.

      | Example: ``{"artist":["Peeping Tom","Amon Tobin"],"title":"Don't Even Trip"}``
    '''
    content = request.get_json(silent=True)
    if content is None:
        return jsonify(fail(msg="No data sent in request!"))
    #pp(content)
    songs = JUKE.songlist.get_songs_by_keyword(**content)
    #pp([s._serialize() for s in songs])
    for song in songs:
        songpath = song.filename
        if os.path.isfile(songpath):
            JUKE.playlist.append(song)
        else:
            return jsonify(fail("%s file does not exist."%songpath))
        print "Added %s"%songpath
        print "Starting Jukebox"
    JUKE.start_jukebox()
    song_titles = [s.title for s in songs]
    return jsonify(succ(value=song_titles))

@app.route('/add_random', methods = ['POST'])
def add_random():
    '''
    Add a random song to the current playlist.

    All arguments should be sent as data in a single json object.

    Args:
      content (Optional(dict)): Request should include, as data, a series of key:value pairs
        corresponding to jukeberry.catalog.Song() attributes.

      | Example: ``{"genre":"Holiday"}``
    '''
    content = request.get_json(silent=True)
    print "Random: {}".format(content)
    song = JUKE.songlist.get_random_song(**content)
    if song is None:
        return jsonify(fail("No matching songs found."))
    songpath = song.filename
    if os.path.isfile(songpath):
        JUKE.playlist.append(song)
    else:
        return jsonify(fail("%s file does not exist."%songpath))
    print "Randomly added %s"%songpath
    print "Starting Jukebox"
    JUKE.start_jukebox()
    return jsonify(succ(value=song.title))

## Start/Stop
@app.route('/start')
def start():
    '''
    Start Jukebox! 
    '''
    JUKE.start_jukebox()
    return "Jukebox Started!"

def succ(field='data',value=''):
    ''' 
    Generates standard JSON reply of the form::

        {'stat':'ok', 'data':{} }
    '''
    return {'stat':'ok',field:value}

def fail(msg='',code=0):
    ''' 
    Generates standard JSON reply of the form::

        {'stat':'fail', 'err':{'msg':'', 'code':0} } 
    '''
    err = {'msg':msg,'code':code}
    return {'stat':'fail','err':err}

def main():
    '''
    Runs when module is called as a script.
    '''
    import sys
    JUKE.load_catalog()
    if 'debug' in sys.argv:
        print "Flask DEBUG"
        app.run(debug = True)
    else:
        print "Flask Production"
        app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
