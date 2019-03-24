# -*- coding: utf-8 -*-
"""Module to manage the songs.
"""

from __future__ import print_function, absolute_import

import os
import time
import json
import eyed3
import eyed3.mp3
import random

from . import utils

class Song(object):
    '''
    Song object. Holds attributes and methods for songs.

    All attributes are derived from ID3 data in the mp3 file.

    Args:
      filename (str): Fully qualified path to song on disk.
      artist (Optional[List[str]]): List of artists.
        From ID3 tag, split on '/'.
      title (Optional[str]): Song title
      album (Optional[str]): Name of album.
      genre (Optional[List[str]]): List of genres.
        From ID3 tag, split on '/'.
      year (Optional[str]): Release year.
      secs (Optional[int]): Length of song in seconds.

    Attributes:
      filename (str): Fully qualified path to song on disk.
      album (str): Name of album.
      artist (List[str]): List of artists.
      title (str): Song title.
      genre (List[str]): List of genres.
      year (str): Release year.
      secs (int): Length of song in seconds.
      hms (str): Length of song as 'mm:ss'.
      id (str): Not used.
    '''

    def __init__(self, filename,
        artist = None,
        title = None,
        album = None,
        genre = None,
        year = None,
        secs = 0):
        if artist is None:
            artist = []
        if genre is None:
            genre = []
        self.filename = filename
        self.artist = artist
        self.title = title
        self.album = album
        self.genre = genre
        self.year = year
        self.secs = secs
        self.hms = ''
        self.id = None
        if type(self.secs) == int:
            self.hms = utils.secs2ms(self.secs)

    def ismatch(self, f, v):
        '''
        Checks to see if song instance is a match to the given
        field=value pair.

        If the attribute is a list and the value (v) is also a list,
        then a ``true`` value is only returned if both lists are the same.

        If the attribute is a list, but the value (v) is not a list,
        then a ``true`` value is returned if the value (v) matches one or more
        items in the attribute.

        Example::

          song1 = Song(filename,artist=['Frank Sinatra', 'Luciano Pavarotti'], title='My Way')
          song2 = Song(filename,artist=['Frank Sinatra'], title='My Way')

          song1.match('artist','Frank Sinatra') # True
          song2.match('artist','Frank Sinatra') # True
          song1.match('artist',['Frank Sinatra', 'Luciano Pavarotti']) # True
          song2.match('artist',['Frank Sinatra', 'Luciano Pavarotti']) # FALSE

        Args:
          f (str): Attribute of song to search on.
          v (str): Value of `f` attribute to constitute a match.

        Returns:
          bool: True if match; False if not.
        '''
        val = getattr(self, f, None)
        ## This way, I can match on genre and artist
        ## Of course, if they are both lists, then 
        ## I'll assume that you are looking for an exact match.
        ## e.g.
        ## If you want to match on the Sinatra version of My Way
        ## but exclude any duets of the same song.
        if isinstance(val, (list, tuple)) and not isinstance(v, (list, tuple)):
            return v in val
        return v == val

    def _serialize(self, fields=None, skip=None):
        retval = {}
        if fields is None:
            fields = self.__dict__.keys()
        if skip is None:
            skip = []
        for f in fields:
            if f in skip:
                continue
            retval[f] = getattr(self,f,None)
        return retval

    def save(self):
        pass

class SongCatalog(list):
    """A list of Song() objects.

    ``get_`` methods of this class that take args return exact matches.

    ``find_`` methods of this class that take args return substring matches.
    """
    def __init__(self, *args, **kwargs):
        super(SongCatalog, self).__init__(*args, **kwargs)

    def index(self, path, verbosity=0):
        """Index .mp3 files in a directory.

        This will recursively scan a given directory for
        .mp3 music files and store them as Song() objects.

        Args:
          path (str): Directory path to music library.
          verbosity (Optional[int]): The verbosity level to output results.

        .. todo:
           Replace verbosity ``print`` with logger.
        """
        if not path.endswith("/"):
            path += "/"
        listing = os.listdir(path)
        songs = []
        for filename in listing:
            filename = path + filename
            if os.path.isdir(filename):
                self.index(filename + "/", verbosity)
            elif filename.endswith(".mp3"):
                if verbosity >= 2:
                    print("Indexing file " + filename)
                song = self.add_song(filename)
                if song is not None:
                    songs.append(song)
        return songs

    def append(self, song, *args, **kwargs):
        """Add Song() object to list if it does not already exist.

        Args:
          song (Song): A Song() object.
          args: Positional args to send to parent class.
          kwargs: Keyward args to send to parent class.

        .. todo:
           Replace verbosity ``print`` with logger.
        """
        if type(song) != Song:
            print("WTF: Not a Song()")
            return None
        if self.find_song(song.filename):
            print("WTF: {} already cataloged".format(song.filename))
            return None
        return super(SongCatalog, self).append(song, *args, **kwargs)

    def find_song(self, song):
        """Find Song() in list based on filename.

        Args:
          song (str): Full path of filename of song to find.

        Returns:
          Song: Song() object. Returns None if not found.

        .. todo:
           Replace verbosity ``print`` with logger.
        """
        filename = song
        if type(song) == Song:
            filename = Song.filename
        retval = None
        songs = [s for s in self if s.filename == filename]
        if len(songs) > 0:
            retval = songs[0]
        return retval

    def add_song(self, filename):
        """Adds song to list from filename.

        Args:
          filename (str): Full path of filename of song.

        Returns:
          Song: Song() object of song that was added.
            Returns None if there was a problem.

        .. todo:
           Replace verbosity ``print`` with logger.

        .. todo:
           Raise errors instead of ``print`` and ``return None``
        """
        asciifilename = filename.encode('ascii', 'ignore')
        print("Adding {}".format(asciifilename))
        if self.find_song(filename):
            print("WTF: {} already cataloged".format(asciifilename))
            return None
        try:
            ismp3 = eyed3.mp3.isMp3File(filename)
        except UnicodeDecodeError:
            ismp3 = False
        if ismp3 is not True:
            print("WTF: {} is not an Mp3File".format(asciifilename))
            return None
        id3 = None
        try:
            id3=eyed3.load(filename)
        except:
            print("WTF: eyed3.load({}) failed".format(asciifilename))
            return None
        if id3 is None:
            return None
        if getattr(id3,'tag',None) is None:
            return None
        genre = getattr(id3.tag,'genre',None)
        if genre:
            genre = genre.name
        else:
            genre = ''
        tags = {
            "artist": id3.tag.artist,
            "title": id3.tag.title,
            "album": id3.tag.album,
            "genre": genre,
            "year": id3.tag.artist,
            "secs": id3.info.time_secs,
        }
        if not tags["artist"] or not tags["title"]:
            print("Artist or title not set in " + \
                filename + " - skipping file")
            return None
        song = Song(filename,
            artist=tags["artist"].split('/'),
            album=tags["album"],
            genre=tags["genre"].split('/'),
            title=tags["title"],
            year=tags["year"],
            secs=tags["secs"],
        )
        #print("WTF: added %s"%song.title)
        self.append(song)
        #print("WTF: That makes",len(self),"songs")
        return song

    def list_all_songs_by_artist(self):
        """Retrieve a hash table of all songs indexed by artist.

        Returns:
          dict: { <artist>: <songs[]> }
        """
        d = {a:self.get_songs_by_artist(a) for a in self.list_artists()}
        return d

    def get_songs_by_keyword(self, **kwargs):
        """Retrieve a list of songs that match key:val pairs.

        Args:
          kwargs: k:v pairs of Song() attributes to match

        Returns:
          list[Song]: List of songs whose attributes match kwargs.
        """
        if len(kwargs.keys()) == 0:
            return []
        apl = [s for s in self]
        for f in kwargs.keys():
            v = kwargs[f]
            apl = [s for s in apl if s.ismatch(f,v)]
        return apl

    def list_artists(self):
        """Retrieve a set of artists.

        Returns:
          set[str]: A unique set of all artists in catalog.
        """
        artists = set();
        for s in self:
            artists.update(s.artist)
        return artists

    def get_songs_by_artist(self, artist):
        """Returns a list of songs by exact match of artist.

        Because the artist attribute is stored as a list, this will match if 
        given artist is one of them. i.e. This will match all solos and duets 
        featuring the artist.

        Args:
          artist (str): Artist to match

        Returns:
          list[Song]: A list of songs by artist
        """
        songs = [s for s in self if artist.lower() in [a.lower() for a in s.artist]]
        return songs 

    def get_random_song(self, **kwargs):
        """Finds a random song from the Catalog matching kwargs.

        Args:
          kwargs: Song attributes to match for list of songs from 
            which to pick a random one.

        Returns:
          Song: A random song.
        """
        songs = self
        print("get_random_song({})".format(kwargs))
        if len(kwargs.keys()) > 0:
            songs = self.get_songs_by_keyword(**kwargs)
        num_songs = len(songs)
        if num_songs < 1:
            return None
        song_num = random.randint(0, num_songs-1)
        song = songs[song_num]
        return song

    def find_songs_by_artist(self, artist):
        """Returns a list of songs by substring match.

        Args:
          artist (str): Artist for which to search for songs.

        Returns:
          list[Song]: List of matching songs.
        """
        songs = [s for s in self if artist.lower() in ''.join(s.artist).lower()]
        return songs 

if __name__ == '__main__':
    ''' test module '''
    stime = time.time()
    medialib = '/var/media/music/'
    catalog = SongCatalog()
    catalog.index(medialib)
    etime = time.time()
    dtime = etime-stime
    print()
    print()
    print(len(catalog),"songs cataloged in",dtime,"seconds.")
