from django import forms
from .models import Tag

class GameForm(forms.Form):
    game = forms.CharField(
        label='Search game',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': 'only english title'})

    )