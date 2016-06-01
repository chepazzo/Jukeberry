#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import unittest
from jukeberry.server import app

class APITestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        ## populate data

    def test_get_artists(self):
        rv = self.app.get('/get/artists')
        ## assert placeholder. Need to make this real
        self.assertEqual('', rv.data)

    def test_get_playlists(self):
        rv = self.app.get('/get/playlists')
        ## assert placeholder. Need to make this real
        self.assertEqual('', rv.data)

    def test_get_songs(self):
        rv = self.app.get('/get/songs')
        ## assert placeholder. Need to make this real
        self.assertEqual('', rv.data)

    def test_get_currsong(self):
        rv = self.app.get('/get/currsong')
        ## assert placeholder. Need to make this real
        self.assertEqual('', rv.data)

    def test_get_alwayson(self):
        rv = self.app.get('/get/alwayson')
        ## assert placeholder. Need to make this real
        self.assertEqual('', rv.data)

    def test_set_alwayson(self):
        rv = self.app.post('/set/alwayson')
        ## assert placeholder. Need to make this real
        self.assertEqual('', rv.data)

    def test_add(self):
        rv = self.app.post('/add')
        ## assert placeholder. Need to make this real
        self.assertEqual('', rv.data)

    def test_add_random(self):
        rv = self.app.post('/add_random')
        ## assert placeholder. Need to make this real
        self.assertEqual('', rv.data)

if __name__ == '__main__':
    unittest.main()
