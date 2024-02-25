# home/urls.py
from django.urls import path
from .views import home
from .views import recommend_movies

urlpatterns = [
    path('', home, name='home'),
    path('recommendations/', recommend_movies, name='recommend_movies'),
]