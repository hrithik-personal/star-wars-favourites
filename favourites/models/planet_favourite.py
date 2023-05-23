from django.db import models
from users import models as users_models
from utils.db_core import BaseAppModel


class PlanetFavourite(BaseAppModel):

    user = models.ForeignKey(users_models.User, on_delete=models.CASCADE)
    swapi_url = models.URLField(max_length=255)
    custom_name = models.CharField(max_length=255, **BaseAppModel.default_empty)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'swapi_url'], name='unique_user_planet')
        ]

    def __str__(self):
        return self.custom_name or self.swapi_url
