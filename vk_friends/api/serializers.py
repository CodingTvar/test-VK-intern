from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from friends.models import User, Profile, FriendshipRequest
from friends.validators import username_validator, validate_of_date


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.MAX_LENGTH_USERNAME,
        required=True
    )

    def validate_username(self, value):
        if (
            isinstance(self, UserSerializer)
            and User.objects.filter(username=value).exists()
        ):
            raise serializers.ValidationError(
                f'Пользователь с именем {value} уже существует'
            )
        return username_validator(value)


class UserSerializer(UsernameSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ProfileSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    friends = UserSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'friends', 'date_update', 'date_create')
        read_only_fields = ('user',)

    def validate_date_update(self, data):
        return validate_of_date(data)


class FriendshipRequestSerializer(serializers.ModelSerializer):
    sender = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    recipient = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = FriendshipRequest
        fields = ('id', 'sender', 'recipient', 'status_req', 'date_update', 'date_sending')
        read_only_fields = ('sender',)

    def validate(self, data):
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        friendship_id = self.context.get('view').kwargs.get('id')
        friendship = get_object_or_404(FriendshipRequest, pk=friendship_id)
        recipient = 0
        if friendship.fr_sender.filter(recipient=recipient):
            raise serializers.ValidationError(
                'Вы не можете отправлять '
                'больше одной заявки в друзья'
            )
        return data
