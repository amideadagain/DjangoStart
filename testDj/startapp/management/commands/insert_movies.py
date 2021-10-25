from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from datetime import datetime

from startapp.models import Movie, Actor  # Role


class Command(BaseCommand):

    help = 'Add new movie(s) to DB'

    def add_arguments(self, parser):
        parser.add_argument('-l', '--len', type=int, default=10)

    def handle(self, *args, **options):

        faker = Faker()

        self.stdout.write('Start inserting movies')
        for _ in range(options['len']):
            self.stdout.write('')
            self.stdout.write('Start inserting movies')

            movie = Movie()
            actor = Actor()

            new_title = ' '.join(faker.text().split()[:randint(2, 6)])
            movie.title = new_title
            movie.plot = faker.text()
            movie.year = randint(1970, datetime.today().year)
            movie.runtime = randint(60, 180)
            movie.rating = randint(0, 3)
            movie.save()

            for _ in range(randint(1, 10)):
                actor.first_name = ' '.join(faker.name().split()[:1])
                actor.last_name = ' '.join(faker.name().split()[1:])
                actor.save()
                movie.actors.add(actor)

            self.stdout.write(f'New movie: {movie}')
        self.stdout.write('End inserting movies')
