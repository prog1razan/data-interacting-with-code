# pylint: disable-all

import unittest
import sqlite3
from yaml import load, FullLoader
from os import path
from memoized_property import memoized_property
import subprocess

from queries import directors_count, directors_list, river_movies,\
    directors_named_like_count, movies_longer_than

with open(path.join(path.dirname(__file__), 'results.yml'), encoding='utf-8') as f:
    results = load(f, Loader=FullLoader)

class TestMovieQueries(unittest.TestCase):

    @memoized_property
    def stubs(self):
        # Download the database
        subprocess.call(
            [
                "curl", "https://wagon-public-datasets.s3.amazonaws.com/sql_databases/movies.sqlite", "--output",
                "data/movies.sqlite"
            ])

    def setUp(self):
        super().setUp()
        self.stubs
        conn = sqlite3.connect('data/movies.sqlite')
        self.db = conn.cursor()

    def test_river_movies_list_is_list(self):
        response = river_movies(self.db)
        self.assertIsInstance(response, list)

    def test_river_movies_list_size(self):
        river_movies_list = results['river_movies']
        response = river_movies(self.db)
        self.assertEqual(len(response), len(river_movies_list))

    def test_river_movies_list_is_sorted(self):
        response = river_movies(self.db)
        sorted_response = sorted(response)
        self.assertEqual(response, sorted_response)

    def test_river_movies_list_is_complete(self):
        river_movies_list = results['river_movies']
        response = river_movies(self.db)
        self.assertEqual(response, river_movies_list)

    def test_river_movies_list_excludes_driver(self):
        response = river_movies(self.db)
        self.assertNotIn("Taxi Driver", response)

    def test_movies_longer_than_list_is_list(self):
        response = movies_longer_than(self.db, 300)
        self.assertIsInstance(response, list)

    def test_movies_longer_than_list_size(self):
        long_movies = results['long_movies']
        response = movies_longer_than(self.db, 300)
        self.assertEqual(len(response), len(long_movies))

    def test_movies_longer_than_list_is_sorted(self):
        response = movies_longer_than(self.db, 300)
        sorted_response = sorted(response)
        self.assertEqual(response, sorted_response)

    def test_movies_longer_than_list_is_complete(self):
        long_movies = results['long_movies']
        response = movies_longer_than(self.db, 300)
        self.assertEqual(response, long_movies)
