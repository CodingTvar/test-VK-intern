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
# from rest_framework import status
from rest_framework.response import Response

from api.permissions import (
    IsAdmin,
    IsAdminAuthorOrReadOnly,
    IsAdminOrReadOnly,
)
from api.serializers import (
    UserSerializer,
    ProfileSerializer,
)
from friends.models import User, Profile, FriendshipRequest


class SignUpViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#    permission_classes = (AllowAny,)

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
#    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'GET':
            return Response(self.get_serializer(request.user).data)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileViewSet():
    http_method_names = ('get', 'post', 'delete', 'patch')
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'
#    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class FriendshipRequestViewSet():
    pass
