from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_extensions.mixins import NestedViewSetMixin

from startapp.models import Movie, MovieManager, Actor, Vote, VoteManager
from .serializers import MovieSerializer, ActorSerializer, VoteSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class MovieViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    filterset_fields = ['title', 'year']
    ordering_fields = ['year', 'title']
    ordering = ['-year']

    @method_decorator(cache_page(60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60))
    @action(methods=['get'], detail=False, name='Top movies')
    def top(self, request, limit=10):
        queryset = Movie.objects.top_movies(limit=limit)
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)


class VoteViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def update(self, request, parent_lookup_movie_id, pk=None):
        pk = parent_lookup_movie_id
        queryset = Vote.objects.api_get(pk)

        serializer = VoteSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

# it isn't in a task, added this as a tool
# class ActorViewSet(viewsets.ModelViewSet):
#     queryset = Actor.objects.all()
#     serializer_class = ActorSerializer
