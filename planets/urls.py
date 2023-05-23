from django.urls import path
from .views import PlanetListView


app_name = 'planets'


urlpatterns = [
    path('', PlanetListView.as_view(), name='planet-list'),
]
