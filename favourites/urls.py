from django.urls import path
from .views import AddMovieFavouriteView, AddPlanetFavouriteView, MovieFavouriteListView, PlanetFavouriteListView

app_name = 'favourites'

urlpatterns = [
    path('movies/add/', AddMovieFavouriteView.as_view(), name='add-movie-favorite'),
    path('planets/add/', AddPlanetFavouriteView.as_view(), name='add-planet-favorite'),
    path('movies/', MovieFavouriteListView.as_view(), name='movie-favorites-list'),
    path('planets/', PlanetFavouriteListView.as_view(), name='planet-favorites-list'),
]
