from django.urls import include, path


urlpatterns = [
    path('movies/', include('movies.urls')),
    path('planets/', include('planets.urls')),
    path('favourites/', include('favourites.urls')),
    path('users/', include('users.urls')),
]
