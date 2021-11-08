from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action

from startapp.models import Movie, MovieManager, Actor
from .serializers import MovieSerializer, ActorSerializer


class MovieList(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        movies = [movie.title for movie in Movie.objects.all()]
        return Response(movies)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def paginate_movies_api(self, request, queryset):
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = MovieSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = MovieSerializer(queryset, many=True)
            return Response(serializer.data)

    def list(self, request):
        queryset = Movie.objects.all()
        return self.paginate_movies_api(request, queryset)

    def create(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Movie.objects.api_get(pk)

        serializer = MovieSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = Movie.objects.api_get(pk)

        serializer = MovieSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    @action(methods=['get'], detail=False, name='Top movies')
    def top(self, request, limit=10):
        queryset = Movie.objects.top_movies(limit=limit)
        return self.paginate_movies_api(request, queryset)


# it isn't in a task, added this as a tool
# class ActorViewSet(viewsets.ModelViewSet):
#     queryset = Actor.objects.all()
#     serializer_class = ActorSerializer