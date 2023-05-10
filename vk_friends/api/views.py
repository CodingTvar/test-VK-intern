from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    # mixins,
    serializers,
    status,
    # views,
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
    RejectedRequestSerializer,
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
    http_method_names = ('get', 'post', 'delete', 'patch')
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
#    lookup_field = 'user'
    # IsAdminAuthorOrReadOnly c аутентификацией
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return ProfileCreateUpdateSerializer
        return ProfileSerializer


class GetDeleteFriendViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'delete')
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        # Переделать, работает не правильно
        profile = get_object_or_404(Profile, pk=self.kwargs.get('profile_id'))
        return profile.get_friends()

    def destroy(self, request, *args, **kwargs):
        # serializer_prof = ProfileSerializer(data=request.data)
        # serializer_req = FriendshipRequestSerializer(
        #    data=FriendshipRequest.objects.filter(sender=request.user))
        return Response()


class SendRequestsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FriendshipRequestSerializer
    # IsAdminAuthor с аутентификацией
    permission_classes = (AllowAny,)

    def get_user(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return FriendshipRequest.objects.filter(sender=self.get_user())

    @action(
        detail=False,
        methods=['POST'],
        url_path=r'(?P<recipient_id>\d+)/send_request',
    )
    def send_request(self, request, *args, **kwargs):
        data = {
            'sender': self.get_user(),
            'recipient': get_object_or_404(User, pk=self.kwargs.get('recipient_id')),
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


class IncomeRequestsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FriendshipRequestSerializer
    # IsAdminAuthor с аутентификацией
    permission_classes = (AllowAny,)

    def get_user(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return FriendshipRequest.objects.filter(recipient=self.get_user())

    @action(
        detail=False,
        methods=['POST'],
        url_path=r'(?P<request_id>\d+)/accept_request',
    )
    def accept_request(self, request, *args, **kwargs):
        accept_req = get_object_or_404(FriendshipRequest, pk=self.kwargs.get('request_id'))
        data = {
            'sender': accept_req.get_sender(),
            'recipient': accept_req.get_recipient(),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        sender = serializer.validated_data['sender']
        recipient = serializer.validated_data['recipient']
        try:
            frequest = FriendshipRequest.objects.create(
                sender=recipient,
                recipient=sender,
                status_req='send',
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {'message': 'Такая заявка уже есть'}
            )
        frequest.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['PATCH'],
        url_path=r'(?P<request_id>\d+)/reject_request',
    )
    def reject_request(self, request, *args, **kwargs):
        get_req = get_object_or_404(FriendshipRequest, pk=self.kwargs.get('request_id'))
        data = {
            'sender': get_req.get_sender(),
            'recipient': get_req.get_recipient(),
            'status_req': get_req.get_status_req(),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        sender = serializer.validated_data['sender']
        recipient = serializer.validated_data['recipient']
        try:
            rej_req = FriendshipRequest.objects.filter(
                sender=sender,
                recipient=recipient,
                status_req='send',
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {'message': 'Такая заявка уже есть'}
            )
        rej_req.update(status_req='rejected')
        return Response(serializer.data)
