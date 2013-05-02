
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from moviesearch.models import Movie, Actor
from moviesearch import api

def index(request):

	movie_list = [] # Movie list 
	
	q = request.GET.get('q', '')
	search_on = request.GET.get('search_on', 'rt')

	search_sources = {'rt': 'Rotton Tomatoes', 'imdb': 'IMDB'}
	api_result = False

	if q:
		# First we'll search in our local database
		# In case we don't find record in our db then we'll make api call to RottonTomatoes or IMDB
		try:
			movie_list = [Movie.objects.get(title=q)]
			#import pdb;  pdb.set_trace();
		except Movie.DoesNotExist:
			movie_list = api.get_movies(q, search_on)			
			api_result = True


	context = {'q': q, 'api_result': api_result, 'search_on': search_on, 'search_sources': search_sources, 'movie_list': movie_list}

	return render(request, 'moviesearch/index.html', context)

def movie(request, movie_id, search_on = 'rt'):

	if movie_id:

		try:
			movie = Movie.objects.get(movie_id=movie_id)
			#import pdb;  pdb.set_trace();
			actors = movie.actors.all()
		except Movie.DoesNotExist:
			movie = api.get_movie_detail(movie_id, search_on)
			api.save_movie(movie, search_on)
			movie = Movie.objects.get(movie_id=movie_id)

		context = {'movie': movie, 'search_on': search_on}


		return render(request, 'moviesearch/movie.html', context)

	return HttpResponseRedirect('/')