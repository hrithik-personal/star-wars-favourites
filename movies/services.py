from .types import MovieTypedDict
from favourites.models.movie_favourite import MovieFavourite
from typing import List, Optional
from users import dao as users_dao
from utils import redis_core
import requests
from .constants import MovieAPIUrls


class MovieListService:

    def transform_movies_from_swapi_response(self, swapi_response: dict, user: users_dao.User) -> List[MovieTypedDict]:
        """
        # Transforms SWAPI's standard response to list of :movies.types.MovieTypedDict:
        # Marks User's favourited movies as favourite and replaces Movie's title with User's custom title, if any

        :raises None:
        """
        movies_list: List[MovieTypedDict] = []
        try:
            for result in swapi_response.get('results', []):
                movie_dict: MovieTypedDict = {
                    'title': result['title'],
                    'release_date': result['release_date'],
                    'created': result['created'],
                    'updated': result['edited'],
                    'url': result['url'],
                    'is_favourite': False
                }
                movie_favourite_obj = MovieFavourite.objects.get_or_none(user=user, swapi_url=result['url'])
                if movie_favourite_obj:
                    movie_dict['is_favourite'] = True
                    if movie_favourite_obj.custom_title:
                        movie_dict['title'] = movie_favourite_obj.custom_title
                movies_list.append(movie_dict)
        except Exception:
            pass
        finally:
            return movies_list
    

    def get_movies_list(self, user: users_dao.User, search_title: Optional[str]) -> List[MovieTypedDict]:
        """
        # Fetches a list of Star Wars movies, either from in-memory cache or SWAPI OpenAPIs
        1. If full list view:
            1.1 Checks first in Redis, if hit returns SWAPI's saved response
            1.2 If Cache miss, fetches data from SWAPI, stores in Redis and returns response
        2. If movie title based search:
            2.1 Checks in :favourites.models.movie_favourite.MovieFavourite: for custom_titles
            2.2 If found in class fetches from SWAPI using :swapi_url: field in class
            2.3 If not found, calls SWAPI list search API and returns response
        
        :raises requests.exceptions.JSONDecodeError: If the response body does not contain valid json.
        """
        movies_list: List[MovieTypedDict] = []

        if search_title is None:
            swapi_movies_data = {}

            # Checking in cache
            cache_key = 'swapi_movies_list'
            cached_data = redis_core.cache_get(cache_key)
            if cached_data:
                swapi_movies_data = cached_data
            # If cache miss, get Movie details from SWAPI apis
            else:
                response = requests.get(MovieAPIUrls.MOVIE_LIST_URL.value)
                swapi_movies_data = response.json()
                # Setting cache for 1 day
                redis_core.cache_set(key=cache_key, data=swapi_movies_data, ttl=24 * 60 * 60)
            movies_list = self.transform_movies_from_swapi_response(swapi_response=swapi_movies_data, user=user)

        else:
            movie_favourite_qset = MovieFavourite.objects.filter(custom_title__icontains=search_title)
            if movie_favourite_qset:
                for movie_favourite in movie_favourite_qset:
                    response = requests.get(movie_favourite.swapi_url)
                    swapi_movies_data = response.json()
                    transformed_movie_list = self.transform_movies_from_swapi_response(swapi_response={'results': [swapi_movies_data]}, user=user)
                    movies_list.extend(transformed_movie_list)
            else:
                response = requests.get(MovieAPIUrls.MOVIE_SEARCH_URL.value + search_title)
                swapi_movies_data = response.json()
                movies_list = self.transform_movies_from_swapi_response(swapi_response=swapi_movies_data, user=user)
        
        return movies_list
