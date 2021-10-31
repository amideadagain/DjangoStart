from uuid import uuid4

from django.db import models
from django.conf import settings
from django.db.models.aggregates import Sum


class Actor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        ordering = ["first_name"]

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class MovieManager(models.Manager):
    def full_length_movies(self, time):
        return self.filter(runtime__gt=time)

    def top_movies(self, limit=10):
        qs = self.get_queryset()
        qs = qs.annotate(vote_sum=Sum("vote__value"))
        qs = qs.exclude(vote_sum=None)
        qs = qs.order_by("-vote_sum")
        qs = qs[:limit]
        return qs

    def all_about_movie(self):
        qs = self.get_queryset()
        qs = qs.annotate(vote_sum=Sum("vote__value"))
        return qs


class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, "NR - Not Rated"),
        (RATED_G, "G - General Audiences"),
        (RATED_PG, "PG - Parental Guidance"),
        (RATED_R, "R - Restricted")
    )

    title = models.CharField(max_length=100)
    plot = models.TextField()
    year = models.PositiveSmallIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField(default=120)
    actors = models.ManyToManyField(Actor, blank=True)

    # actors = models.ManyToManyField(
    #     Actor,
    #     through="Role",
    #     through_fields=("actor", "movie"),
    #     blank=True
    # )
    objects = MovieManager()

    class Meta:
        ordering = ["-year", "title"]

    def __str__(self):
        return "{} ({})".format(self.title, self.year)


# class Role(models.Model):
#     actor = models.ForeignKey(Actor, on_delete=models.SET_NULL)
#     movie = models.ForeignKey(Movie, on_delete=models.SET_NULL)
#     character_name = models.CharField(max_length=50)


def movie_directory_path_with_uuid(instance, filename):
    return "{}/{}.{}".format(instance.movie_id, uuid4(), filename.split(".")[-1])


# class MovieImage(models.Model):
#     image = models.ImageField(upload_to=movie_directory_path_with_uuid)
#     uploaded = models.DateTimeField(auto_now_add=True)
#     movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class VoteManager(models.Manager):
    # def get_vote_or_unsaved_blank_vote(self, movie, user):
    def get_vote_or_unsaved_blank_vote(self, movie):
        try:
            return Vote.objects.get(movie=movie)
            # return Vote.objects.get(movie=movie, user=user)
        except Vote.DoesNotExist:
            return Vote(movie=movie)
            # return Vote(movie=movie, user=user)


class Vote(models.Model):
    UP = 1
    DOWN = -1
    VOTE_CHOICES = (
        (
            UP,
        ),
        (
            DOWN,
        )
    )
    value = models.IntegerField(default=0)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    objects = VoteManager()
