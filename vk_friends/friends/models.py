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
        return self.username[:settings.TEXT_STR]


class Profile(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Владелец профиля',
        on_delete=models.CASCADE,
    )
    friends = models.ManyToManyField(
        User,
        verbose_name='Друзья',
        related_name='friends',
        blank=True,
    )
    date_update = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True
    )
    date_create = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self) -> str:
        return self.user[:settings.TEXT_STR]


STATUS_CHOICES = (
    ('', ''),
    ('', ''),
    ('', ''),
)


class FriendshipRequest(models.Model):
    sender = models.ForeignKey(
        User,
        verbose_name='Имя отправителя',
        related_name='fr_sender',
        on_delete=models.CASCADE,
    )
    recipient = models.ForeignKey(
        User,
        verbose_name='Имя получателя',
        related_name='fr_recipient',
        on_delete=models.CASCADE,
    )
    status_req = models.CharField(
        verbose_name='',
        max_length=settings.MAX_STATUS,
        choices=STATUS_CHOICES,
    )
    date_update = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True,
    )
    date_sending = models.DateTimeField(
        verbose_name='Дата отправки',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sender', 'recipient'],
                                    name='unique_sender_recipient')
        ]
        ordering = ('sender',)
        verbose_name = 'Заявка в друзья'
        verbose_name_plural = 'Заявки в друзья'

    def __str__(self) -> str:
        return (f'Заявка в друзья от {self.sender[:settings.TEXT_STR]} '
                f'отправлена {self.recipient[:settings.TEXT_STR]} '
                f'со статусом {self.recipient[:settings.TEXT_STR]}')
