import os

from mutagen.easyid3 import EasyID3
import eyeD3
#from mutagen.mp3 import MP3, HeaderNotFoundError
#from mutagen.id3 import ID3NoHeaderError

def index(path,verbosity=0):
    if not path.endswith("/"):
        path += "/"
    indexer = FileIndexer()
    listing = os.listdir(path)
    for filename in listing:
        filename = path + filename
        if os.path.isdir(filename):
            self.index(filename + "/", verbosity)
        elif filename.endswith(".mp3"):
            if verbosity >= 2:
                print "Indexing file " + filename
            indexer.index(filename)

class SongList(list):
    def __init__(self,*args, **kwargs):
        super(list, self).__init__(*args, **kwargs)
    def find_song(self,filename):
        songs = [s for s in self if s.filename == filename]
        return songs

class Song(object):
    def __init__(self,filename,
        artist = None,
        title = None,
        album = None,
        genre = None,
        year = None):
        self.filename = filename
        self.artist = artist
        self.title = title
        self.album = album
        self.genre = genre
        self.year = year
        #
        self.id = None

    def save(self):
        pass

class SongCatalog(object):

    def __init__(self):
        songs = []

    def add_song(self, filename):
        # skip already indexed
        if eyeD3.isMp3File(filename) is not True:
            return
        if self.is_indexed(filename):
            return
        id3 = eyeD3.Tag()
        id3.link(filename)
        tags = {
            "artist": id3.getArtist(),
            "title": id3.getTitle(),
            "album": id3.getAlbum(),
            "genre": id3.getGenre().name,
            "year": id3.getYear(),
        }
        if not tags["artist"] or not tags["title"]:
            print "Artist or title not set in " + \
                filename + " - skipping file"
            return

        song = Song(filename
            artist=tags["artist"],
            album=tags["album"],
            genre=tags["genre"],
            title=tags["title"],
            year=tags["date"],
        )
        song.save()

    def delete(self, filename):
        # single file
        Song.objects.filter(Filename__exact=filename).delete()
        # directory
        Song.objects.filter(Filename__startswith=filename).delete()

    def is_indexed(self, filename):
        data = Song.objects.filter(Filename__exact=filename)
        if not data:
            return False
        return True
