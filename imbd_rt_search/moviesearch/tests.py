
from django.test import TestCase

from moviesearch.models import Movie


class MovieMethodTest(TestCase):
    def test_movie_exist(self):
    	"""
   		test_movie_exist should return if movie Titanic already in the database
    	"""
    	
        self.assertEqual(Movie.objects.filter(title='Titanic'), True)
