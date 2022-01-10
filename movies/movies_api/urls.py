from django.urls import include, path
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import views


router = ExtendedDefaultRouter()
# movies route
(
    router.register(r'movies', views.MovieViewSet, basename='movies')
          .register(r'vote',
                    views.VoteViewSet,
                    'movies-vote',
                    parents_query_lookups=['movie_id'])
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]