import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


def handle_api_exc(func):
    '''Decorator for APIs to handles exceptions (including serialiser.is_valid(raise_exception=True)) and logging.'''

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValidationError, exceptions.NotFound, ObjectDoesNotExist, AssertionError) as e:
            return JsonResponse({'error': str(e)}, safe=False, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': 'Favourite already exists.'}, status=400, safe=False)
        except Exception as e:
            logger.critical(str(e), exc_info=True)
            return JsonResponse({'error': 'Some error occured.'}, status=500, safe=False)

    return wrapper
