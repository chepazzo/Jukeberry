#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Runs main server.
"""
from __future__ import print_function, absolute_import

import sys
import argparse
from .conf import settings
from . import server
import sys

def main():
    args = get_args()
    ##
    autoload = settings.GLOBAL['AUTOLOAD']
    debug = settings.GLOBAL['DEBUG']
    threaded = settings.GLOBAL['THREADED']
    ##
    if debug:
        print("Flask DEBUG")
    else:
        print("Flask Production")
    if autoload:
        print("AUTOLOAD")
        server.JUKE.load_catalog()
    if settings.GLOBAL['SSL'] == True:
        context = (settings.SSL['SSL_CRT'], settings.SSL['SSL_KEY'])
        print("running flask: host={}, port={}, debug={}, ssl_context={}, threaded={}".format(settings.WEB['HOST'], settings.WEB['PORT'], debug, context, threaded))
        server.app.run(host=settings.WEB['HOST'], port=settings.WEB['PORT'], debug=debug, ssl_context=context, threaded=threaded)
    else:
        print("running flask: host={}, port={}, debug={}, threaded={}".format(settings.WEB['HOST'], settings.WEB['PORT'], debug, threaded))
        server.app.run(host=settings.WEB['HOST'], port=settings.WEB['PORT'], debug=debug, threaded=threaded)

def get_args():
    args = get_parser().parse_args()
    settings.load(args.i)
    ## If args set in cmdline, override in settings.
    if args.ssl is not None:
        settings.GLOBAL['SSL'] = args.ssl
    if args.threaded is not None:
        settings.GLOBAL['THREADED'] = args.threaded
    if args.crt is not None:
        settings.SSL['SSL_CRT'] = args.crt
    if args.key is not None:
        settings.SSL['SSL_KEY'] = args.key
    if args.debug is not None:
        settings.GLOBAL['DEBUG'] = args.debug
    if args.autoload is not None:
        settings.GLOBAL['AUTOLOAD'] = args.autoload
    return args

def get_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", default='/etc/ipapi.conf', help="Specify config file")
    parser.add_argument('--autoload', action='store_true', default=None, help="Autoload lib at startup")
    parser.add_argument('--debug', action='store_true', default=None, help="Enable debug mode")
    parser.add_argument('--ssl', dest='ssl', action='store_true', default=None, help="Enable ssl")
    parser.add_argument('--no-ssl', dest='ssl', action='store_false', default=None, help="Disable ssl")
    parser.add_argument('--thread', dest='threaded', action='store_true', default=None, help="Enable threading")
    parser.add_argument('--no-thread', dest='threaded', action='store_false', default=None, help="Disable threading")
    parser.add_argument('--crt', default=None, help="Path to ssl crt")
    parser.add_argument('--key', default=None, help="Path to ssl key")
    return parser

if __name__ == '__main__':
    main()
