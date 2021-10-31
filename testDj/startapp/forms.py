from django import forms
from django.contrib.auth import get_user_model
from .models import Vote, Movie  # MovieImage


class VoteForm(forms.ModelForm):

    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True
    )
    movie = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Movie.objects.all(),
        disabled=True
    )
    value = forms.FloatField()

    class Meta:
        model = Vote
        fields = (
            'user',
            'movie',
            'value'
        )


# class MovieImageForm(forms.ModelForm):
