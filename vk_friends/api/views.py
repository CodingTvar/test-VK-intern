from django.conf import settings
from django.db import IntegrityError
# from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    mixins,
    serializers,
    status,
    views,
    viewsets
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
    UsernameSerializer,
)
from friends.models import User, Profile, FriendshipRequest


class SignUpView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        try:
            user, _ = User.objects.get_or_create(username=username,)
        except IntegrityError:
            raise serializers.ValidationError(
                {'message': 'Пользователь с такими данными уже существует'}
            )
        user.save()
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'delete', 'patch')
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminOrReadOnly,)
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
    pass


class FriendshipRequestViewSet():
    pass
