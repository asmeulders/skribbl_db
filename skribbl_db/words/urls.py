from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('words/', views.words, name='words'),
    path('words/details/<int:id>', views.details, name='details'),
    path('words/new_word/', views.new_word, name='new_word'),
    path('wordsets/', views.new_wordset, name='new_wordset')
]
