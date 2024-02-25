# home/urls.py
from django.urls import path
from .views import home
from .views import recommend_movies
from .views_api import home_api
from .views_api import recommend_movies_api
from .views_api import update_train_data_api

urlpatterns = [
    path('', home, name='home'),
    path('recommendations/', recommend_movies, name='recommend_movies'),
    path('api/home/', home_api, name='home_api'),  # Adjust view_api for import
    path('api/recommend_movies/', recommend_movies_api, name='recommend_movies_api'), 
    path('api/update_train_data_api/', update_train_data_api, name='update_train_data_api'),  # Adjust view_api for import
]