#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This library controls the function of the jukebox player.
'''

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
PLAYER = 'omxplayer'
'''
 Filesystem executable to use to play music.
 Jukeberry will search the filesystem (``which ${PLAYER}``) for the fq path.

 BTW, omxplayer has MUCH better sound quality than mpg123 on Raspi.

 I should probably make this an env variable
  or a config option where default setup
  would look for the existance of omxplayer (raspi only)
  and set the env var appropriately, but could be
  overwritten by an option in a /etc/jukeberry.conf file
  (default=default).
'''
LIB = '/var/media/music/'
'''
 Directory of music library.

 TODO: I should probably make this an env variable or a config option.
'''

class Jukebox(object):
    '''
    Main Jukebox object.

    Args:
      player (Optional[str]): Filesystem executable to use to play music.
        Jukeberry will search the filesystem (``which ${PLAYER}``) for the fq path.
        Default is from global.
      medialib (Optional[str]): Directory of music library.
        Default is from global.

    Attributes:
      player (str): Fully qualified path to filesystem executable to use to play music.
      medialib (str): Fully qualified path to directory of music library.
      songlist (catalog.SongCatalog): List of all songs loaded from medialib.
      playlist (List[catalog.Song]): List of songs in queue.
      alwayson (Dict[str,any]): The alwayson filter data.

        Dict Structure:
          status (bool): Is the Jukebox always on? If so, then a random song will play
            if the queue is empty.
          filter (Dict[str,str]): This will filter the list of songs available to be
            randomly selected to play (if the filter is on), where the ``key`` is an
            attribute of ``catalog.Song``.

      currsong (catalog.Song): Reference to instance of the currently playing song.
      proc (subprocess.Popen): Stores the ``subprocess.Popen`` instance for currently
        playing song.

    .. todo:: Change proc to currthread and store thread here so I can monitor it with ``currthread.is_alive()``.

    '''
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
        '''
        Invoke the ``catalog.SongCatalog.index`` function to 
          scan the ``medialib`` for songs.
        '''
        stime = time.time()
        self.songlist.index(self.medialib)
        etime = time.time()
        dtime = etime-stime
        print
        print
        print len(self.songlist),"songs cataloged in",dtime,"seconds."

    def start_jukebox(self):
        '''
        Start the Jukebox by playing the next song in the queue.
        If a song is already playing, then do nothing.
        '''
        ## Start playing assuming there
        ## is no song already playing
        if self.currsong is None:
            self.play_next_song()

    def play_next_song(self):
        '''
        Plays the next song in the queue and updates the ``currsong`` attribute.

        This is meant to be the callback function when the current song finishes
          playing.

        '''
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
        '''
        Adds songs to playlist by keyword.

        Args:
          **kwargs: keys for keyword arguments should be an attribute of ``catalog.Song``.
        '''
        songs = self.catalog.get_songs_by_keyword(**kwargs)
        self.playlist.extend(songs)

    def get_next_song(self):
        '''
        Retrieves the next song in the playlist and removes it from the playlist.

        Returns:
          catalog.Song: The next song in the playlist.
          None: If no songs in list.
        '''
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
