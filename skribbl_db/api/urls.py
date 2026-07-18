from django.urls import path
from .views import WordsView, WordSetView


urlpatterns = [
    path('words/', WordsView.as_view(), name='words'),
    path('words/wordset', WordSetView.as_view(), name='word_set')
]