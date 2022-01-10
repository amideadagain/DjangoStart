from django.test import TestCase

from startapp.models import Movie, Actor, Vote


class MovieTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Movie.objects.create(title='Test Film',
                             plot='Stuff happens',
                             year='2021',
                             runtime='135')
        Movie.objects.create(title='Test Film 2',
                             plot='Stuff happens again',
                             year='2022',
                             runtime='40')
        Movie.objects.create(title='Test Film 3',
                             plot='Future',
                             year='2222',
                             runtime='200')
        Vote.objects.create(value=5, movie=Movie.objects.get(id=1))
        Vote.objects.create(value=10, movie=Movie.objects.get(id=2))

    def test_movie_model_str(self):
        movie = Movie.objects.get(id=1)
        self.assertEqual(str(movie), 'Test Film (2021)')

    def test_vote_model_str(self):
        movie = Movie.objects.get(id=1)
        vote = Vote.objects.get(movie=movie)
        self.assertEqual(str(vote), '5')

    def test_full_length_movies_filter(self):
        filtered = Movie.objects.full_length_movies(time=100)
        self.assertEqual(str(filtered), '<QuerySet [<Movie: Test Film 3 (2222)>, <Movie: Test Film (2021)>]>')

    def test_top_movies_filter(self):
        qs = Movie.objects.top_movies(2)
        self.assertEqual(str(qs), '<QuerySet [<Movie: Test Film 2 (2022)>, <Movie: Test Film (2021)>]>')

    # def test_all_about_movie(self):
    #     qs = Movie.objects.all_about_movie()

    def test_get_vote_or_unsaved_blank_vote(self):
        movie1 = Movie.objects.get(id=1)
        movie2 = Movie.objects.get(id=3)
        vote1 = Vote.objects.get_vote_or_unsaved_blank_vote(movie1)
        vote2 = Vote.objects.get_vote_or_unsaved_blank_vote(movie2)
        self.assertEqual(str(vote1), '5')
        self.assertEqual(str(vote2), '0')


class ActorTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Actor.objects.create(first_name='Kiara',
                             last_name='Takanashi')

    def test_actor_model_str(self):
        actor = Actor.objects.get(id=1)
        self.assertEqual(str(actor), 'Kiara Takanashi')
