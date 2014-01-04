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

class FileIndexer:
    def index(self, filename):
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

        if tags["artist"]:
            tags["artist"], created = Artist.objects.get_or_create(
                Name=tags["artist"]
            )
        if tags["album"] is not None and tags["artist"] is not None:
            tags["album"], created = Album.objects.get_or_create(
                Title=tags["album"]
            )
        if tags["genre"] is not None:
            tags["genre"], created = Genre.objects.get_or_create(
                Name=tags["genre"]
            )
        if tags["date"] is not None:
            try:
                tags["date"] = int(tags["date"])
            except ValueError:
                tags["date"] = None

        audio = MP3(filename)
        tags["length"] = int(audio.info.length)

        song = Song(
            Artist=tags["artist"],
            Album=tags["album"],
            Genre=tags["genre"],
            Title=tags["title"],
            Year=tags["date"],
            Length=tags["length"],
            Filename=filename
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
