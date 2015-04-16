#!/usr/bin/env python
from jukeberry import server
import sys

def main():
    #server.JUKE.medialib = '/var/media/music/Misc/'
    #server.JUKE.load_catalog()
    if 'debug' in sys.argv:
        print "Flask DEBUG"
        server.app.run(debug = True)
    else:
        print "Flask Production"
        server.app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
