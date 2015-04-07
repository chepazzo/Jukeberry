import os
import time
import json
import eyed3
import eyed3.mp3
import utils

class Song(object):

    def __init__(self,filename,
        artist = None,
        title = None,
        album = None,
        genre = None,
        year = None,
        secs = 0):
        if artist is None:
            artist = []
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

    def _serialize(self,fields=None,skip=None):
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
    def __init__(self,*args, **kwargs):
        super(SongCatalog, self).__init__(*args, **kwargs)

    def index(self,path,verbosity=0):
        if not path.endswith("/"):
            path += "/"
        listing = os.listdir(path)
        for filename in listing:
            filename = path + filename
            if os.path.isdir(filename):
                self.index(filename + "/", verbosity)
            elif filename.endswith(".mp3"):
                if verbosity >= 2:
                    print "Indexing file " + filename
                self.add_song(filename)

    def append(self,song,*args,**kwargs):
        if type(song) != Song:
            print "WTF: Not a Song()"
            return None
        if self.find_song(song.filename):
            print "WTF: %s already cataloged"%song.filename
            return None
        return super(SongCatalog, self).append(song,*args,**kwargs)

    def find_song(self,song):
        filename = song
        if type(song) == Song:
            filename = Song.filename
        retval = None
        songs = [s for s in self if s.filename == filename]
        if len(songs) > 0:
            retval = songs[0]
        return retval

    def add_song(self, filename):
        print "Adding %s"%filename
        if self.find_song(filename):
            print "WTF: %s already cataloged"%filename
            return None
        try:
            ismp3 = eyed3.mp3.isMp3File(filename)
        except UnicodeDecodeError:
            ismp3 = False
        if ismp3 is not True:
            print "WTF: %s is not an Mp3File"%filename
            return None
        id3 = None
        try:
            id3=eyed3.load(filename)
        except:
            print "WTF: eyed3.load(%s) failed"%filename
            return None
        if id3 is None:
            return None
        if getattr(id3,'tag',None) is None:
            return None
        genre = getattr(id3.tag,'genre',None)
        if genre:
            genre = genre.name
        tags = {
            "artist": id3.tag.artist,
            "title": id3.tag.title,
            "album": id3.tag.album,
            "genre": genre,
            "year": id3.tag.artist,
            "secs": id3.info.time_secs,
        }
        if not tags["artist"] or not tags["title"]:
            print "Artist or title not set in " + \
                filename + " - skipping file"
            return None
        song = Song(filename,
            artist=tags["artist"].split('/'),
            album=tags["album"],
            genre=tags["genre"],
            title=tags["title"],
            year=tags["year"],
            secs=tags["secs"],
        )
        #print "WTF: added %s"%song.title
        self.append(song)
        #print "WTF: That makes",len(self),"songs"
        return song

    def list_all_songs_by_artist(self):
        d = {a:self.get_songs_by_artist(a) for a in self.list_artists()}
        return d

    def get_songs_by_keyword(self,**kwargs):
        apl = [s for s in self]
        for f in kwargs.keys():
            v = kwargs[f]
            apl = [s for s in apl if getattr(s,f,None) == v]
        return apl

    def list_artists(self):
        artists = set();
        for s in self:
            artists.update(s.artist)
        return artists

    def get_songs_by_artist(self,artist):
        ''' Returns list of songs by exact match '''
        songs = [s for s in self if artist.lower() in [a.lower() for a in s.artist]]
        return songs 

    def find_songs_by_artist(self,artist):
        ''' Returns list of songs by substring match '''
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
    print
    print
    print len(catalog),"songs cataloged in",dtime,"seconds."
