from django.test import Client, TestCase
from django.urls import reverse
from random import randint

from startapp.views import MovieList
from movies_auth.models import MyUser as User
from startapp.models import Movie


class MovieListTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Creating 12 movies for pagination tests
        """
        number_of_movies = 12
        for movie_number in range(number_of_movies):
            Movie.objects.create(
                title='Test Film {}'.format(movie_number),
                plot='Stuff happens',
                year=f'{2000 + movie_number}',
                runtime=f'{randint(60, 180)}'
            )

    def test_view_url_get(self):
        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'startapp/movie_list.html')

    def test_pagination_equals_ten(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['movie_list']) == 10)

    def test_lists_all_movies(self):
        response = self.client.get(reverse('movie-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['movie_list']) == 2)


# class CreateMovieTestCase(TestCase):
#
#     def setUp(self):
#         self.factory = RequestFactory(enforce_csrf_checks=True)
#         self.user = User.objects.create_user(
#             username='TestDude',
#             email='testmail@gmail.com',
#             dob='2000-01-08',
#             password='testword'
#         )
#
#     def test_create_movie(self):
#         data = {
#             'title': 'Test Film 3',
#             'plot': 'Future',
#             'year': '2222',
#             'runtime': '200'
#         }
#         request = self.factory.post('/movies', data=data, content_type='application/json')
#         request.user = self.user
#
#         response = MovieList.as_view()(request)
#         print(response)
#         self.assertEqual(response.status_code, 200)
#         print(Movie.objects.all())


class CreateMovieTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        # self.user = User.objects.create_user(
        #     username='TestDude',
        #     email='testmail@gmail.com',
        #     dob='2000-01-08',
        #     password='testword'
        # )

    def test_create_movie(self):
        data = {
            'title': 'Test Film',
            'plot': 'Future',
            'rating': 1,
            'year': 2022,
            'runtime': 150
        }
        # response = self.client.post('/auth/', {'username': 'TestDude', 'password': 'testword'})
        # print(response.status_code)

        response = self.client.post('/movies', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Movie.objects.get(title="Test Film"))

    def test_create_incorrect_movie(self):
        data = {
            'plot': 'Future',
            'year': '2222',
            'runtime': '200'
        }
        response = self.client.post('/movies', data=data)
        self.assertFormError(response, 'form', 'title', 'This field is required.')
