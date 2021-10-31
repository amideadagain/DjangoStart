from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='startapp-home'),
    path('movies', views.MovieList.as_view(), name='movie-list'),
    path('movies/top', views.TopMovies.as_view(), name='top-movies'),
    path('movies/top/<int:limit>', views.TopMovies.as_view(), name='top-movies'),
    path('movies/<int:pk>', views.MovieDetail.as_view(), name='movie-detail'),
    path('movie/<int:movie_id>/vote', views.CreateVote.as_view(), name='create-vote'),
    path('movie/<int:movie_id>/vote/<int:pk>',
         views.UpdateVote.as_view(),
         name='update-vote'
         ),
    # path('movie/<int:movie_id>/image/upload', views.MovieImageUpload.as_view(), name='movie-image-upload')
]
