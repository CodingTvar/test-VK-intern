from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    mixins,
    serializers,
    status,
    views,
    viewsets,
    generics,
)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.permissions import IsAdminOrReadOnly
from api.serializers import (
    UserSerializer,
    ProfileSerializer,
    ProfileCreateUpdateSerializer,
    FriendshipRequestSerializer,
)
from friends.models import User, Profile, FriendshipRequest


class SignUpViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'delete', 'patch')
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class ProfileViewSet(viewsets.ModelViewSet):
    http_method_names = ('get','post', 'delete', 'patch')
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'
    permission_classes = (AllowAny,) # IsAdminAuthorOrReadOnly c аутентификацией

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return ProfileCreateUpdateSerializer
        return ProfileSerializer


class GetDeleteFriendViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'delete')
    serializer_class = UserSerializer
    lookup_field = 'user'
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Profile.friends.filter(pk=self.kwargs.get('profile_id'))

    def destroy(self, request, *args, **kwargs):
        serializer_prof = ProfileSerializer(data=request.data)
        serializer_req = FriendshipRequestSerializer(
            data=FriendshipRequest.objects.filter(sender=request.user))
        return Response()


class RequestsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FriendshipRequestSerializer
    permission_classes = (AllowAny,) # IsAdminAuthor с аутентификацией

    def get_user(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return FriendshipRequest.objects.filter(sender=self.get_user())

    @action(
        detail=False,
        methods=['POST']
    )
    def send_request(self, request, **kwargs):
        data={
            'sender': self.get_user(),
            'recipient': self.request.data['recipient'],
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        sender = serializer.validated_data['sender']
        recipient = serializer.validated_data['recipient']
        try:
            frequest = FriendshipRequest.objects.create(
                sender=sender,
                recipient=recipient,
                status_req='send',
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {'message': 'Такая заявка уже есть'}
            )
        frequest.save()
        return Response(serializer.data)