from rest_framework import serializers
from startapp.models import Movie, Actor, Vote


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    year = serializers.IntegerField(min_value=1900, max_value=2100)
    runtime = serializers.IntegerField(min_value=0, max_value=500)
    actors = serializers.StringRelatedField(many=True)
    vote = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = ['title', 'plot', 'year', 'rating', 'runtime', 'actors', 'vote']


class VoteSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vote
        fields = ['value', 'movie_id']


class ActorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actor
        fields = ['first_name', 'last_name']
