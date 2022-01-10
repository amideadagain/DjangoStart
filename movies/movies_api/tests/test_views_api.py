from rest_framework.test import APITestCase, APIRequestFactory,  force_authenticate
from django.urls import reverse
from random import randint

from movies_auth.models import MyUser as User
from startapp.models import Movie
from movies_api.views import MovieViewSet


class MovieViewSetListTestCase(APITestCase):
    url = reverse('movies_api:movies-list')

    @classmethod
    def setUpTestData(cls):
        """
        Creating 12 movies for pagination tests
        """
        number_of_movies = 12
        for movie_number in range(number_of_movies):
            Movie.objects.create(
                title='Test Film {}'.format(movie_number + 1),
                plot='Stuff happens',
                year=f'{2000 + movie_number}',
                runtime=f'{randint(60, 180)}'
            )

    def test_movie_list_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        response = self.client.get(self.url)
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 12)
        self.assertFalse(data['next'] is None)
        self.assertTrue(data['previous'] is None)
        self.assertEqual(len(data['results']), 10)

    def test_second_page(self):
        url = self.url + '?page=2'
        response = self.client.get(url)
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['next'] is None)
        self.assertFalse(data['previous'] is None)
        self.assertEqual(len(data['results']), 2)

    # def test_create_movie_post_unauthorised(self):
    #     data = {
    #         "title": "Mad scientist girl",
    #         "plot": "Republican rest up..",
    #         "year": 1985,
    #         "rating": 3,
    #         "runtime": 179,
    #         "actors": [],
    #         "vote": []
    #     }
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, 401)


class CreateMovieTestCase(APITestCase):
    url = reverse('movies_api:movies-list')

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='TestDude',
            email='testmail@gmail.com',
            dob='2000-01-08',
            password='testword'
        )
        self.create_view = MovieViewSet.as_view(actions={'post': 'create'})

    def test_create_movie_post(self):
        data = {
            "title": "Mad scientist girl",
            "plot": "Republican rest up..",
            "year": 1985,
            "rating": 3,
            "runtime": 179,
            "actors": [],
            "vote": []
        }
        request = self.factory.post(self.url, data, format='json')
        force_authenticate(request, user=self.user)
        response = self.create_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Movie.objects.get(title="Mad scientist girl"))

    def test_create_movie_post_unauthorised(self):
        data = {
            "title": "Mad scientist girl",
            "plot": "Republican rest up..",
            "year": 1985,
            "rating": 3,
            "runtime": 179,
            "actors": [],
            "vote": []
        }
        request = self.factory.post(self.url, data, format='json')
        response = self.create_view(request)
        self.assertEqual(response.status_code, 401)

    def test_create_incorrect_movie_data_post(self):
        data = {
            "title": "",
            "plot": "",
            "year": -200,
            "rating": 10,
            "runtime": -10,
            "actors": [],
            "vote": []
        }
        request = self.factory.post(self.url, data, format='json')
        force_authenticate(request, user=self.user)
        response = self.create_view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.data)
        self.assertIn('plot', response.data)
        self.assertIn('year', response.data)
        self.assertIn('rating', response.data)
        self.assertIn('runtime', response.data)
