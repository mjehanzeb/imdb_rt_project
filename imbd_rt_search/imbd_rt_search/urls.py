from django.conf.urls import patterns, include, url
from moviesearch import views


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'imbd_rt_search.views.home', name='home'),
    # url(r'^imbd_rt_search/', include('imbd_rt_search.foo.urls')),

    url(r'^$', 'moviesearch.views.index'),
    url(r'^movie/(?P<movie_id>\w+)/source/(?P<search_on>\w+)/$', views.movie, name='movie_detail'),
    #url(r'^movie/(?P<movie_id>\d+)/$', views.movie, name='movie_detail'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
