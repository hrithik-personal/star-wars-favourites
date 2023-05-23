from .models import User
from django.core.exceptions import ValidationError


def validate_user(user_id: int) -> User:
    try:
        user_obj = User.objects.get(id=user_id)
        return user_obj
    except User.DoesNotExist:
        raise ValidationError(f"User not found with User ID: {user_id}")
