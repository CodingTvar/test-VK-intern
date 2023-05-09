from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from djoser.serializers import UserSerializer


from friends.models import User, Profile, FriendshipRequest
from friends.validators import username_validator, validate_of_date


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=settings.MAX_LENGTH_USERNAME,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username',)

    def validate_username(self, value):
        if (
            isinstance(self, UserSerializer)
            and User.objects.filter(username=value).exists()
        ):
            raise serializers.ValidationError(
                f'Пользователь с именем {value} уже существует'
            )
        return username_validator(value)


class ProfileCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    friends = UserSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Profile
        fields = ('user', 'friends', 'date_update', 'date_create')

    def validate(self, data):
        if data == ('date_update' or 'date_create'):
            return validate_of_date(data)
        return data


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        read_only=True,
    )
    friends = UserSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Profile
        fields = ('user', 'friends', 'date_update', 'date_create')

    def validate(self, data):
        if data == ('date_update' or 'date_create'):
            return validate_of_date(data)
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        profile_id = self.context.get('view').kwargs.get('id')
        profile = get_object_or_404(Profile, pk=profile_id)
        if profile.objects.filter(user=request.user):
            raise serializers.ValidationError(
                'Вы не можете создать '
                'больше одного профиля'
            )
        return data


class FriendshipRequestSerializer(serializers.ModelSerializer):
    sender = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    recipient = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = FriendshipRequest
        fields = ('sender', 'recipient', 'status_req', 'date_update', 'date_sending')
        read_only_fields = ('sender',)

    def validate(self, data):
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        friendship_id = self.context.get('view').kwargs.get('id')
        friendship = get_object_or_404(FriendshipRequest, pk=friendship_id)
        recipient = friendship.fr_recipient.filter(sender=request.user)
        if friendship.fr_sender.filter(recipient=recipient):
            raise serializers.ValidationError(
                'Вы не можете отправлять '
                'больше одной заявки в друзья'
            )
        return data
