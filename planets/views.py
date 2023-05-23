
import requests
from . import constants
from django.views import View
from .types import PlanetTypedDict
from users import dao as users_dao
from django.http import JsonResponse
from rest_framework.views import APIView
from .serializers import PlanetSerializer
from rest_framework.response import Response
from utils.error_handlers import handle_api_exc
from . import services


class PlanetListView(View):

    @handle_api_exc
    def get(self, request):
        user_id = request.GET.get("user_id")
        page = request.GET.get("page", 1)
        search_name = request.GET.get("search_name")

        # Validating if user exists
        user = users_dao.validate_user(user_id)

        planets_list = services.PlanetListService().get_planets_list(user=user, search_name=search_name, page=page)

        serializer = PlanetSerializer(data=planets_list, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)
