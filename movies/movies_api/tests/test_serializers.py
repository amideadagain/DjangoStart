from django.test import TestCase

from movies_api.serializers import MovieSerializer
from startapp.models import Movie, Actor, Vote


class MovieSerializerTestCase(TestCase):

    def test_serializer(self):
        movie1 = Movie.objects.create(
            title='Test Film',
            plot='Stuff happens',
            year=2021,
            rating=1,
            runtime=135
        )
        movie2 = Movie.objects.create(
            title='Test Film 2',
            plot='Stuff happens again',
            year=2022,
            rating=1,
            runtime=40
        )
        data = MovieSerializer([movie1, movie2], many=True).data
        expected_data = [
            {
                "title": "Test Film",
                "plot": "Stuff happens",
                "year": 2021,
                "rating": 1,
                "runtime": 135,
                "actors": [],
                "vote": []
            },
            {
                "title": "Test Film 2",
                "plot": "Stuff happens again",
                "year": 2022,
                "rating": 1,
                "runtime": 40,
                "actors": [],
                "vote": []
            }
        ]
        self.assertEqual(data, expected_data)