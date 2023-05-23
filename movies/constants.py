from enum import Enum
from star_wars_favourites import settings


class MovieAPIUrls(Enum):

    BASE_URL = settings.SWAPI_BASE_URL
    MOVIE_LIST_ENDPOINT = '/api/films/'
    MOVIE_SEARCH = '/api/films/?search='

    MOVIE_LIST_URL = BASE_URL + MOVIE_LIST_ENDPOINT
    MOVIE_SEARCH_URL = BASE_URL + MOVIE_SEARCH
