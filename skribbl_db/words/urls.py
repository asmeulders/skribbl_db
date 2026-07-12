from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('words/', views.words, name='words'),
    path('words/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),   
]
