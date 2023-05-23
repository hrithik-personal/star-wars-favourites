from django.db import models
from users import models as user_models
from utils.db_core import BaseAppModel
from django.contrib.auth import get_user_model


class MovieFavourite(BaseAppModel):
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    swapi_url = models.URLField(max_length=255)
    custom_title = models.CharField(max_length=255, **BaseAppModel.default_empty)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'swapi_url'], name='unique_user_movie')
        ]

    def __str__(self):
        return self.custom_title or self.swapi_url
