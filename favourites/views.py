from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MovieFavouriteSerializer, PlanetFavouriteSerializer
from .models import MovieFavourite, PlanetFavourite
from django.shortcuts import get_object_or_404
from users.models import User
from utils.error_handlers import handle_api_exc


class AddMovieFavouriteView(APIView):

    @handle_api_exc
    def post(self, request):
        user_id = request.data.get("user_id")

        user = get_object_or_404(User, id=user_id)
        serializer = MovieFavouriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(serializer.data)
    
    def put(self, request):
        try:
            user_id = request.data.get("user_id")
            swapi_url = request.data.get("swapi_url")
            movie_favourite = MovieFavourite.objects.get(user_id=user_id, swapi_url=swapi_url)
        except MovieFavourite.DoesNotExist:
            return Response({'error': 'MovieFavourite not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieFavouriteSerializer(movie_favourite, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddPlanetFavouriteView(APIView):

    @handle_api_exc
    def post(self, request):
        serializer = PlanetFavouriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def put(self, request):
        try:
            user_id = request.data.get("user_id")
            swapi_url = request.data.get("swapi_url")
            planet_favourite = PlanetFavourite.objects.get(user_id=user_id, swapi_url=swapi_url)
        except PlanetFavourite.DoesNotExist:
            return Response({'error': 'PlanetFavourite not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlanetFavouriteSerializer(planet_favourite, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MovieFavouriteListView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        # Check if user exists
        user = get_object_or_404(User, id=user_id)
        # Get movie favourites for the user
        movie_favourites = user.moviefavourite_set.all()  # Access the related movie favorites
        # Serialize the movie favourites
        serializer = MovieFavouriteSerializer(movie_favourites, many=True)

        return Response(serializer.data)

class PlanetFavouriteListView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        # Check if user exists
        user = get_object_or_404(User, id=user_id)
        # Get planet favourites for the user
        planet_favourites = PlanetFavourite.objects.filter(user=user).all()
        # Serialize the planet favourites
        serializer = PlanetFavouriteSerializer(planet_favourites, many=True)

        return Response(serializer.data)
