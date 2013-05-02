# This will house all operations related to RottenTomatoes API and IMDB api service

import requests

RT_API_KEY = 'v42gy6vz74y2xjaxe7gf92k5' # RottenTomatoes API key
RT_API_BASE_URL = 'http://api.rottentomatoes.com/api/public/v1.0/' # RottenTomatoes API Base URL

IMDB_API_BASE_URL = "http://imdbapi.org"

PAGE_LIMIT = 5

def get_movies(search_term, search_on):

	if search_on == 'rt': 
		search_url = RT_API_BASE_URL + 'movies.json'
		params = {
					'apikey': RT_API_KEY,
					'page_limit': PAGE_LIMIT,
					'q': search_term,
		}
	else:
		search_url = IMDB_API_BASE_URL
		params = {
					'title': search_term,
					'type': 'json',
					'limit': PAGE_LIMIT
		}

		
	response = requests.get(search_url, params=params)

	movies = []
		
	if response.status_code == requests.codes.ok:
		#import pdb;  pdb.set_trace();
		response = response.json()

		if search_on == 'imdb':

			return response

		if response['movies']:
			movies = response['movies']
	
	return movies

def get_movie_detail(movie_id, search_on):

	if search_on == 'rt': 
		movie_url = RT_API_BASE_URL + 'movies/%s.json' %movie_id
		params = {
				'apikey': RT_API_KEY,
		}
	else:
		movie_url = IMDB_API_BASE_URL
		params = {
					'id': movie_id,
					'type': 'json'
		}

	response = requests.get(movie_url, params=params)
	
	movie = {}
		
	if response.status_code == requests.codes.ok:
		if search_on == 'rt':
			movie = format_rt_movie(response.json())
		else:
			movie = format_imdb_movie(response.json())

	return movie

def format_rt_movie(movie_data):
	movie = movie_data
	movie['movie_source'] = 'rt'
	movie['movie_id'] = movie.get('id')
	movie['poster'] = movie.get('posters')['detailed']

	movie['actors'] = []
	#import pdb;  pdb.set_trace();

	return movie

def format_imdb_movie(movie_data):
	movie = movie_data
	movie['movie_source'] = 'imdb'
	movie['movie_id'] = movie.get('imdb_id')
	movie['synopsis'] = movie.get('plot_simple')

	import re
	movie['runtime'] = int(re.search('\d+', movie['runtime'][0]).group())

	return movie


def save_movie(movie, search_on):
	
	from django.utils import simplejson
	from moviesearch import models

	movie_object = models.Movie() # Initialize movie object
	
	for field in models.Movie._meta.fields:
		
		setattr(movie_object, field.name, movie.get(field.name, None))

	#import pdb;  pdb.set_trace();
	m = movie_object.save()
	
	if movie['actors']:
		for actor in movie['actors']:
			actor_object, created = models.Actor.objects.get_or_create(name=actor)
			movie_object.actors.add(actor_object)
	
