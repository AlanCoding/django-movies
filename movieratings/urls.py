"""movieratings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, patterns, url
from django.contrib import admin
from Rater import views as Rater_views
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'Rater.views.handler404'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index.html$', Rater_views.view_index, name="view_index"),
    url(r'^$', Rater_views.view_index, name="view_index"),
#    url(r'^user.html(?P<rater_id>\d+)$', Rater_views.view_user, name="view_user"),
    url(r'^user.html([\d]+)$', Rater_views.UserView.as_view(), name="view_user"),

    url(r'^movie.html(?P<movie_id>\d+)$', Rater_views.view_movie, name="view_movie"),
    url(r'^register.html$', Rater_views.view_register, name="view_register"),
    url(r'^logout.html$', Rater_views.view_logout, name="view_logout"),
    url(r'^login.html$', Rater_views.view_login, name="view_login"),
    url(r'^rating.html(?P<rating_id>\d+)$', Rater_views.view_rating, name="view_rating"),
    url(r'^dashboard.html$', Rater_views.view_dashboard, name="view_dashboard"),
    url(r'^fig(?P<movie_id>\d+).png$', Rater_views.view_fig, name="view_fig"),

#url(r'^genre.html(?P<genre_id>\d+)$', Rater_views.view_genre, name="view_genre"),
#    url(r'^genre.html(?P<genre_id>\d+)$', Rater_views.GenreView.as_view(), name="view_genre"),
    url(r'^genre.html(?P<genre_id>\d+)$', Rater_views.GenreView.as_view(), name="view_genre"),
    url(r'^top20.html$', Rater_views.Top20View.as_view(), name="top_rated_movies"),
    # url(r'^top20.html$', Rater_views.view_top20_movies, name="view_top20_movies"),
    # url(r'^moviebase/best_movies$', moviebase_views.BestMoviesListView.as_view(), name="best_movies")
#    url(r'^confused.html$', Rater_views.view_add_rating, name="view_add_rating"),
    url('^', include('django.contrib.auth.urls'))

#    url(r'^user/(?P<user_id>\d+)$', updates_views.show_user, name="show_user")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
            )
    urlpatterns += patterns('',
                 (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
                 )
