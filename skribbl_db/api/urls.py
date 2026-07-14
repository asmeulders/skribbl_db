from django.urls import path
from .views import WordsView


urlpatterns = [
    path('words/', WordsView.as_view(), name='words'),
]