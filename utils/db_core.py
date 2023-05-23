from django.db import models


class CustomQuerySet(models.QuerySet):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CustomManager(models.Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    def get_or_none(self, **kwargs):
        return self.get_queryset().get_or_none(**kwargs)


class BaseAppModel(models.Model):

    default_empty = {"blank": True, "null": True}

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    deleted_at = models.DateTimeField(editable=False, **default_empty)

    objects = CustomManager()

    class Meta:
        abstract = True

