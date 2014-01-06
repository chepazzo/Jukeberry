#/usr/bin/env python

from flask import Flask, request
import json
import subprocess
import os
import threading
import time
import catalog

from pprint import pprint as pp

playlist = []
## Add files to playlist via POST to /add:
## curl -i -H "Content-Type: application/json" -X POST -d '{"path":"/edia/music/Misc/The Champs - Tequila.mp3"}' http://localhost:5000/add

currsong = None
proc = None
mpg123 = None

fin, fout = os.popen4(["which", "mpg123"])
mpg123 = fout.read().replace("\n", "")

#pygame.mixer.init()
def start_jukebox():
    ## Start playing assuming there
    ## is no song already playing
    if currsong is None:
        play_next_song()

def play_next_song():
    global currsong
    ## Clear current playing song
    currsong = None
    song = get_next_song()
    if song is not None:
        currsong = song
        currthread = _popenAndCall(play_next_song,([mpg123,song],))

def get_next_song():
    global playlist
    songpath = None
    if len(playlist) > 0:
        songpath = playlist[0]
        playlist = playlist[1:]
    return songpath

def _popenAndCall(onExit, popenArgs):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that 
    would give to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs):
        proc = subprocess.Popen(*popenArgs)
        proc.wait()
        onExit()
        return
    thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
    thread.start()
    pp(dir(thread))
    # returns immediately after the thread starts
    return thread

#####
# REST Interface
#####
app = Flask(__name__)

@app.route('/')
def index():
    return "MISHAP JukeBox!"

@app.route('/start')
def start():
    start_jukebox()
    return "Jukebox Started!"

@app.route('/get')
def get_playlist():
    return json.dumps(playlist)

@app.route('/add', methods = ['POST'])
def add():
    global currsong
    global playlist
    if not request.json or not 'path' in request.json:
        abort(400)
    songpath = request.json.get('path',None)
    if os.path.isfile(songpath):
        playlist.append(songpath)
    else:
        return "%s file does not exist."%songpath
    print "Added %s"%songpath
    print "Starting Jukebox"
    start_jukebox()
    return "added",songpath

if __name__ == '__main__':
    stime = time.time()
    medialib = '/opt/OLD/opt/Send Home/KDZ Music/'
    catalog = catalog.SongCatalog()
    catalog.index(medialib)
    etime = time.time()
    dtime = etime-stime
    print
    print
    print len(catalog),"songs cataloged in",dtime,"seconds."
    app.run(debug = True)
