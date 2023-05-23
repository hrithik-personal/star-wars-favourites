from users import dao as users_dao
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MovieSerializer
from utils.error_handlers import handle_api_exc
from . import services



class MovieListView(APIView):

    @handle_api_exc
    def get(self, request):
        user_id = request.GET.get("user_id")
        search_title = request.GET.get("search_title")

        # Validating if user exists
        user = users_dao.validate_user(user_id)

        movies_list = services.MovieListService().get_movies_list(user=user, search_title=search_title)

        serializer = MovieSerializer(movies_list, many=True)
        return Response(serializer.data)
