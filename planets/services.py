from .types import PlanetTypedDict
from typing import List, Optional
from favourites.models.planet_favourite import PlanetFavourite
from users.dao import User
from utils.redis_core import cache_get, cache_set
import json
import requests
from . import constants


class PlanetListService:

    def transform_planets_from_swapi_response(self, swapi_response: dict, user: User) -> List[PlanetTypedDict]:
        """
        # Transforms SWAPI's standard response to list of :planets.types.PlanetTypedDict:
        # Marks User's favourited planets as favourite and replaces Planet's name with User's custom name, if any

        :raises None:
        """
        planets_list: List[PlanetTypedDict] = []
        try:
            for result in swapi_response.get('results', []):
                planet_dict: PlanetTypedDict = {
                    'name': result['name'],
                    'created': result['created'],
                    'updated': result['edited'],
                    'url': result['url'],
                    'is_favourite': False
                }
                planet_favourite_obj = PlanetFavourite.objects.get_or_none(user=user, swapi_url=result['url'])
                if planet_favourite_obj:
                    planet_dict['is_favourite'] = True
                    if planet_favourite_obj.custom_name:
                        planet_dict['name'] = planet_favourite_obj.custom_name
                planets_list.append(planet_dict)
        except Exception:
            pass
        finally:
            return planets_list
        
    
    def get_planets_list(self, user: User, search_name: Optional[str], page: int=1) -> List[PlanetTypedDict]:
        """
        # Fetches a list of Star Wars planets, either from in-memory cache or SWAPI OpenAPIs
        1. If full list view:
            1.1 Checks first in Redis, if hit returns SWAPI's saved response
            1.2 If Cache miss, fetches data from SWAPI, stores in Redis and returns response
        2. If movie title based search:
            2.1 Checks in :favourites.models.planet_favourite.PlanetFavourite: for custom_names
            2.2 If found in class fetches from SWAPI using :swapi_url: field in class
            2.3 If not found, calls SWAPI list search API and returns response
        
        :raises requests.exceptions.JSONDecodeError: If the response body does not contain valid json.
        """
        planets_list: List[PlanetTypedDict] = []

        if search_name is None:
            # Checking in cache
            cache_key = f"planets:{page}"
            cached_data = cache_get(cache_key)
            if cached_data:
                swapi_planets_data = cached_data
            else:
                # If cache miss, get from SWAPI
                params = {"page": page}
                response = requests.get(constants.PlanetAPIUrls.PLANET_LIST_URL.value, params=params)
                swapi_planets_data = json.loads(response.text)
                # Cache data for 1 day (24 * 60 * 60 seconds)
                cache_set(cache_key, swapi_planets_data, 24 * 60 * 60)

            planets_list = []
            for result in swapi_planets_data['results']:
                planet_dict: PlanetTypedDict = {
                    'name': result['name'],
                    'created': result['created'],
                    'updated': result['edited'],
                    'url': result['url'],
                    'is_favourite': False
                }
                planet_favourite_obj = PlanetFavourite.objects.get_or_none(user=user, swapi_url=result['url'])
                if planet_favourite_obj:
                    planet_dict['is_favourite'] = True
                    if planet_favourite_obj.custom_name:
                        planet_dict['name'] = planet_favourite_obj.custom_name
                planets_list.append(planet_dict)
        
        else:
            planet_favourite_qset = PlanetFavourite.objects.filter(custom_name__icontains=search_name)
            if planet_favourite_qset:
                for planet_favourite in planet_favourite_qset:
                    response = requests.get(planet_favourite.swapi_url)
                    swapi_planets_data = response.json()
                    transformed_movie_list = self.transform_planets_from_swapi_response(swapi_response={'results': [swapi_planets_data]}, user=user)
                    planets_list.extend(transformed_movie_list)
            else:
                response = requests.get(constants.PlanetAPIUrls.PLANET_SEARCH_URL.value + search_name)
                swapi_movies_data = response.json()
                planets_list = self.transform_planets_from_swapi_response(swapi_response=swapi_movies_data, user=user)

        return planets_list
