#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the main server module that runs the Flask Server.
"""

from __future__ import print_function, absolute_import

import os
import json
from pprint import pprint as pp

try:
    from flask import Flask, request, jsonify, send_from_directory, Response
    import eyed3
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')
    FLASK_INSTALLED = True
except:
    FLASK_INSTALLED = False

try:
    from . import jukebox
    JUKE = jukebox.Jukebox()
    JUKEBOX_INSTALLED = True
except:
    JUKEBOX_INSTALLED = False

## Helper functions
def succ(field='data',value=''):
    ''' 
    Return a json object indicating success.
    '''
    return {
        'status': 'success',
        field: value
    }

def fail(field='message',msg=''):
    ''' 
    Return a json object indicating failure.
    '''
    return {
        'status': 'fail',
        field: msg
    }

## API Catch-all Route
# This must be the first route defined to catch all non-API paths
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

## API

@app.route('/api/loadcatalog')
def load_catalog():
    '''Loads catalog from disk.'''
    songs = JUKE.load_catalog()
    retval = [s._serialize(skip=['filename']) for s in songs]
    return jsonify(succ(value=retval))

@app.route('/api/get/artists')
def get_artists():
    '''Get a list of artists.'''
    retval=sorted(JUKE.songlist.list_artists())
    return jsonify(succ(value=retval))

@app.route('/api/get/playlist')
def get_playlist():
    '''Get current playlist.'''
    retval = [s._serialize() for s in JUKE.playlist]
    return jsonify(succ(value=retval))

@app.route('/api/get/songs')
def get_songs():
    '''Get all songs.'''
    songs = JUKE.songlist
    retval = [s._serialize() for s in songs]
    return jsonify(succ(value=retval))

@app.route('/api/art/<song_id>')
def get_art(song_id):
    '''Get album art for a given song.'''
    song = JUKE.songlist.get_song_by_id(song_id)
    if song and song.has_art:
        audiofile = eyed3.load(song.filename)
        if audiofile.tag.images:
            image = audiofile.tag.images[0]
            return Response(image.image_data, mimetype=image.mime_type)
    return ('', 204)

@app.route('/api/get/currsong')
def get_currsong():
    '''Get current song.'''
    retval = JUKE.currsong
    if retval is not None:
        retval = retval._serialize()
    return jsonify(succ(value=retval))

@app.route('/api/get/autoplay')
def get_autoplay():
    '''Get the autoplay status.'''
    retval = JUKE.autoplay
    return jsonify(succ(value=retval))

@app.route('/api/set/autoplay', methods=['POST'])
def set_autoplay():
    '''Set the autoplay status.'''
    content = request.get_json(silent=True)
    if content is None:
        return jsonify(fail(msg="No data sent in request!"))
    if 'status' in content:
        JUKE.autoplay['status'] = content['status']
    if 'filters' in content:
        JUKE.autoplay['filters'] = content['filters']
    return jsonify(succ(value=JUKE.autoplay))

@app.route('/api/add', methods=['POST'])
def add():
    '''Add a song to the current playlist.'''
    content = request.get_json(silent=True)
    if content is None:
        return jsonify(fail(msg="No data sent in request!"))
    songs = JUKE.songlist.get_songs_by_keyword(**content)
    for song in songs:
        JUKE.playlist.append(song)
    JUKE.start_jukebox()
    song_titles = [s.title for s in songs]
    return jsonify(succ(value=song_titles))

@app.route('/api/add_random', methods=['POST'])
def add_random():
    '''Add a random song to the current playlist.'''
    content = request.get_json(silent=True) or {}
    song = JUKE.songlist.get_random_song(**content)
    if song is None:
        return jsonify(fail(msg="No songs found matching that criteria"))
    JUKE.playlist.append(song)
    JUKE.start_jukebox()
    return jsonify(succ(value=song.title))

@app.route('/api/rm', methods=['POST'])
def rm():
    '''Remove a song from the playlist.'''
    content = request.get_json(silent=True)
    JUKE.remove_song(content['id'])
    return jsonify(succ())

@app.route('/api/play', methods=['POST'])
def play():
    '''Start playing the jukebox.'''
    JUKE.start_jukebox()
    return jsonify(succ())

@app.route('/api/pause', methods=['POST'])
def pause():
    '''Pause the jukebox.'''
    JUKE.pause_jukebox()
    return jsonify(succ())

@app.route('/api/skip', methods=['POST'])
def skip():
    '''Skip to the next song in the playlist.'''
    JUKE.skip_song()
    return jsonify(succ())

@app.route('/api/volume', methods=['POST'])
def volume():
    '''Set the volume.'''
    content = request.get_json(silent=True)
    JUKE.set_volume(content['level'])
    return jsonify(succ())

@app.route('/api/start')
def start():
    '''Start the jukebox.'''
    JUKE.start_jukebox()
    return jsonify(succ())

@app.route('/api/stop')
def stop():
    '''Stop the jukebox.'''
    JUKE.stop_jukebox()
    return jsonify(succ())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
