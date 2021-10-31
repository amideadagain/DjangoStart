from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse

from .forms import VoteForm
from .models import Movie, Vote


def home(request):
    movies = '<br>\n'.join([str(i) for i in Movie.objects.all()])
    return HttpResponse(f"Films <br> {movies}")


class MovieList(ListView):
    model = Movie
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MovieList, self).get_context_data(**kwargs)
        page = context["page_obj"]
        paginator = context["paginator"]
        context["page_is_first"] = page.number == 1
        context["page_is_last"] = page.number == paginator.num_pages
        return context


class TopMovies(ListView):
    template_name = "startapp/top_movies.html"
    queryset = Movie.objects.top_movies(limit=10)

    def get_queryset(self):
        limit = 10
        qs = Movie.objects.top_movies(limit=limit)
        return qs


class MovieDetail(DetailView):
    queryset = Movie.objects.all_about_movie()

    def post(self, request, *args, **kwargs):
        return redirect('create-vote', movie_id=kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(movie=self.object, user=self.request.user)
            if vote.id:
                vote_form_url = reverse('update-vote', kwargs={'movie_id': vote.movie.id, 'pk': vote.id})
            else:
                vote_form_url = reverse('create-vote', kwargs={'movie_id': self.object.id})
            ctx['vote_form'] = VoteForm(instance=vote)
            ctx['vote_form_url'] = vote_form_url
        return ctx


class CreateVote(LoginRequiredMixin, CreateView):
    model = Vote
    template_name = "startapp/movie_detail.html"
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        print('never called?')
        movie_id = self.kwargs['movie_id']
        return reverse('movie-detail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('movie-detail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)

    def form_valid(self, form):
        vote = form.save(commit=False)
        movie = Movie.objects.get(id=movie_id)
        vote.movie = movie
        vote.save()  # You have to save the vote for it to be added to the db.
        return HttpResponseRedirect(reverse('redirect_view'))


class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied("cannot change")
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse("movie-detail", kwargs={"pk": movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context["object"].id
        movie_detail_url = reverse("movie-detail", kwargs={"pk": movie_id})
        return redirect(to=movie_detail_url)
