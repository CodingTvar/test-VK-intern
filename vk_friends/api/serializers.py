from django.conf import settings
# from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from friends.models import User, Profile, FriendshipRequest, STATUS_CHOICES
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
        queryset=User.objects.all(),
        slug_field='username',
    )
    friends = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        many=True,
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
        if Profile.objects.filter(user=data['user']):
            raise serializers.ValidationError(
                'Вы не можете создавать '
                'больше одного профиля'
            )
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
        return data


class FriendshipRequestSerializer(serializers.ModelSerializer):
    sender = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    recipient = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    status_req = serializers.ChoiceField(
        read_only=True,
        choices=STATUS_CHOICES,)

    class Meta:
        model = FriendshipRequest
        fields = ('id',
                  'sender',
                  'recipient',
                  'status_req',
                  'date_update',
                  'date_sending')
        read_only_fields = ('sender',)

    def validate(self, data):
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        if data['sender'] == data['recipient']:
            raise serializers.ValidationError(
                'Вы не можете отправлять себе заявку в друзья'
            )
        friendship_id = self.context.get('view').kwargs.get('id')
        friendship = FriendshipRequest.objects.filter(pk=friendship_id)
        if friendship.filter(sender=data['sender'],
                             recipient=data['recipient']):
            raise serializers.ValidationError(
                'Вы не можете отправлять '
                'больше одной заявки в друзья'
            )
        return data


class RejectedRequestSerializer(FriendshipRequestSerializer):
    status_req = serializers.ChoiceField(choices=STATUS_CHOICES,)
