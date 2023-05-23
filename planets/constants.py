from enum import Enum
from star_wars_favourites import settings


class PlanetAPIUrls(Enum):

    BASE_URL = settings.SWAPI_BASE_URL
    PLANET_LIST_ENDPOINT = '/api/planets/'
    PLANET_SEARCH = '/api/planets/?search='

    PLANET_LIST_URL = BASE_URL + PLANET_LIST_ENDPOINT
    PLANET_SEARCH_URL = BASE_URL + PLANET_SEARCH
