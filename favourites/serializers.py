from rest_framework import serializers
from .models import MovieFavourite, PlanetFavourite
from users import models as users_models
from django.core.exceptions import ValidationError


class MovieFavouriteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    swapi_url = serializers.URLField()
    custom_title = serializers.CharField(required=False)

    class Meta:
        model = MovieFavourite
        fields = ['user_id', 'swapi_url', 'custom_title']

    def validate_user_id(self, value):
        user = users_models.User.objects.filter(id=value).exists()
        if not user:
            raise ValidationError("Invalid user ID.")
        return value


class PlanetFavouriteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    swapi_url = serializers.URLField()
    custom_name = serializers.CharField(required=False)

    class Meta:
        model = PlanetFavourite
        fields = ['user_id', 'swapi_url', 'custom_name']

    def validate_user_id(self, user_id):
        user_exists: bool = users_models.User.objects.filter(id=user_id).exists()
        if not user_exists:
            raise ValidationError(f"User not found with User ID: {user_id}")
        return user_id
