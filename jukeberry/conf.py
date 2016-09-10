#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is a boilerplate config module to read an INI-style config and export settings.
"""

from __future__ import print_function, absolute_import

import logging
log = logging.getLogger(__name__)

#from backports import configparser
import configparser
 
unicode = str
class Conf(object):
    """Conf object to simplify loading config options from ini files

       Attributes: 
         logi (logging.Logger): Logger instance for class.
         parser (configparser.ConfigParser): ConfigParser object to parse config files. 
         bool_fields (list): List of fields that should be loaded as booleans.
         int_fields (list): List of fields that should be loaded as integers.
         float_fields (list): List of fields that should be loaded as floats.
         cust_fields (dict): List of fields that should be loaded using a custom method.

            | Format: { 'field_name': <method('value')> }

         SECTIONS (dict): Loaded from ``[SECTION]``'s in config file.

    """

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.parser = configparser.ConfigParser()
        self.bool_fields = ['DEBUG']
        self.int_fields = ['PORT']
        self.float_fields = []
        self.cust_fields = {}

    def load(self, conffile=None, confstr=None):
        """Loads configuration from file or string/unicode.
        """
        if confstr is not None:
            try:
                self.parser.read_string(u'{}'.format(confstr))
            except Exception as e: 
                self.log.error( "** Conf String ({}) invalid (debug: {})**".format(confstr, e) )
        if conffile is not None:
            try:
                self.parser.read(conffile)
            except: 
                self.log.error( "** Conf File ({}) invalid **".format(conffile) )
        if confstr is None and conffile is None:
            self.log.error( "** No configuration provided **" )
        if len(self.parser.sections()) < 1:
            self.log.error( "** Config ({}, {}) missing or invalid **".format(conffile, confstr) )
            exit()
        for sectname in self.parser.sections():
            section = {}
            setattr(self,sectname,section)
            opts = self.parser.options(sectname)
            for opt in opts:
                val = self.parser.get(sectname,opt)
                if opt.upper() in self.cust_fields:
                    val = self.cust_fields[opt](val)
                if opt.upper() in self.int_fields:
                    val = self.parser.getint(sectname,opt)
                if opt.upper() in self.bool_fields:
                    val = self.parser.getboolean(sectname,opt)
                if opt.upper() in self.float_fields:
                    val = self.parser.getfloat(sectname,opt)
                section[opt.upper()] =val

settings = Conf()
