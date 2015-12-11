#/usr/bin/env python
# -*- coding: utf-8 -*-

## Add files to playlist via POST to /add:
## curl -i -H "Content-Type: application/json" -X POST -d '{"path":"/edia/music/Misc/The Champs - Tequila.mp3"}' http://localhost:5000/add

#package modules
import catalog
import utils

#other modules
import json
import os
import time
import random

from pprint import pprint as pp

#PLAYER = 'mpg123'
## omxplayer has MUCH better sound quality on Raspi
## I should probably make this an env variable
##  as well as a config option where default setup
##  would look for the existance of omxplayer (raspi only)
##  and set the env var appropriately, but this could be
##  overwritten by an option in the /etc/jukeberry.conf file
##  (default=default).
PLAYER = 'omxplayer'
LIB = '/var/media/music/'

class Jukebox(object):
    def __init__(self,player=None,medialib=None):
        if player is None:
            player = PLAYER
        if medialib is None:
            medialib = LIB
        self.songlist = catalog.SongCatalog()
        self.playlist = []
        self.alwayson = {
            "status":False,
            "filter":{}
        }
        self.currsong = None
        self.proc = None
        self.player = utils.find_player(player)
        self.medialib = medialib

    def load_catalog(self):
        stime = time.time()
        self.songlist.index(self.medialib)
        etime = time.time()
        dtime = etime-stime
        print
        print
        print len(self.songlist),"songs cataloged in",dtime,"seconds."

    def start_jukebox(self):
        ## Start playing assuming there
        ## is no song already playing
        if self.currsong is None:
            self.play_next_song()

    def play_next_song(self):
        ## Clear current playing song
        self.currsong = None
        song = self.get_next_song()
        if song is None:
            if self.alwayson['status']:
                print "No next song ... finding random."
                song = self.songlist.get_random_song(**self.alwayson['filter'])
        filename = None
        if type(song) == catalog.Song:
            filename = song.filename
        else:
            filename = song
        if filename is not None:
            self.currsong = song
            currthread = utils._popenAndCall(self.play_next_song,([self.player,filename],))

    def add_songs_to_playlist(self,**kwargs):
        songs = self.catalog.get_songs_by_keyword(**kwargs)
        self.playlist.extend(songs)

    def get_next_song(self):
        songpath = None
        if len(self.playlist) > 0:
            songpath = self.playlist[0]
            self.playlist = self.playlist[1:]
        return songpath

if __name__ == '__main__':
    jbox = Jukebox()
    import sys
    app.run(debug=True)
    '''
    if 'debug' in sys.argv:
        print "Flask DEBUG"
        app.run(debug = True)
    else:
        print "Flask Production"
        app.run(host='0.0.0.0')
    '''
