from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Movie


def home(request):
    movies = '<br>\n'.join([str(i) for i in Movie.objects.all()])
    return HttpResponse(f" <br> {movies}")


class MovieList(ListView):
    model = Movie
    paginate_by = 10

    def get_context_data(self, **kwargs):
        ctx = super(MovieList, self).get_context_data(**kwargs)
        page = ctx["page_obj"]
        paginator = ctx["paginator"]
        ctx["page_is_first"] = page.number == 1
        ctx["page_is_last"] = page.number == paginator.num_pages
        return ctx
