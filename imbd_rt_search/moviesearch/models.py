
import datetime

from django.db import models
from django.utils import timezone
from django.utils import simplejson


class Actor(models.Model):
 
    name = models.CharField(max_length=100)

    def __unicode__(self):
		return self.name	
  
class Movie(models.Model):
 
    movie_id = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    synopsis = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    runtime = models.IntegerField()
    poster = models.TextField(blank=True, null=True)
    movie_source = models.CharField(max_length=4)

    actors = models.ManyToManyField(Actor)

    @property
    def duration_formatted(self):

       hours = self.runtime/60

       minutes = self.runtime%60
       return "%d hour %s minutes"%(hours, minutes)
    
    @property
    def detailed_poster(self):
        
        posters = dict(simplejson.loads(self.posters))
        #import pdb;  pdb.set_trace();
        return posters['detailed']
    

    def format_movie(self):
        self.id = self.movie_id
        self.posters = dict(simplejson.loads(self.posters))

        return self
    def __unicode__(self):
		return self.title		

   