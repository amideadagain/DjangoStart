from django import forms
from django.contrib.auth import get_user_model
from .models import Vote, Movie  # MovieImage


class VoteForm(forms.ModelForm):

    movie = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Movie.objects.all(),
        disabled=True
    )
    value = forms.IntegerField()

    class Meta:
        model = Vote
        fields = (
            "value",
            "movie",
        )


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = (
            "title",
            "plot",
            "year",
            "rating",
            "runtime",
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'forms-input'}),
            'plot': forms.TextInput(attrs={'cols': 100, 'rows': 30}),
        }
