from django.conf import settings
from django.db import models

from friends.validators import username_validator


class User(models.Model):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.MAX_LENGTH_USERNAME,
        unique=True,
        validators=(username_validator,),
        error_messages={
            'unique': ('Пользователь с таким именем уже существует'),
        },
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

class FriendshipRequest(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='f_requests',
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        User,
        related_name='f_requests',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('sender',)
        verbose_name = 'Заявка в друзья'
        verbose_name_plural = 'Заявки в друзья'

    def __str__(self) -> str:
        return f'Заявка в дрзуья от {self.sender} отправлена {self.recipient}'

class Friends(models.Model):
    pass
