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
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAdmin
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

    def post(self, request, *args, **kwargs):
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
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class ProfileViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'delete', 'patch')
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'
    permission_classes = (AllowAny,) # IsAdminAuthorOrReadOnly c аутентификацией

    def get_serializer_class(self):
        if self.action in ('partial_update'):
            return ProfileCreateUpdateSerializer
        return ProfileSerializer

    def destroy(self, request):
        
        return Response()


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


class ProfileUsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user'
    permission_classes = (IsAuthenticated,)

    @action(detail=False,
            methods=['POST'],
            permission_classes=(IsAuthenticated,),
            url_path=r'(?P<user_id>\d+)/send_request/')
    def send_request(self, request):
        serializer = FriendshipRequestSerializer(
            request.user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        sender = serializer.validated_data['sender']
        recipient = serializer.validated_data['recipient']
        try:
            frequest, _ = FriendshipRequest.objects.create(
                sender=sender,
                recipient=recipient,
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {'message': 'Такая заявка уже есть'}
            )
        frequest.save()
        return Response(serializer.data)

