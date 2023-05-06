import re

from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import ValidationError


def username_validator(value):
    if value in settings.RESTRICTED_USERNAMES:
        raise ValidationError(f"{value} - запрещённое имя пользователя")
    restr_symb = "".join(set(re.findall(r"[^\w.@+-]", value)))
    if restr_symb:
        raise ValidationError(
            f"Недопустимые символы в имени пользователя: {restr_symb}"
        )
    return value