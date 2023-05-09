from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (SignUpViewSet,
                       UserViewSet,
                       ProfileViewSet,
                       GetDeleteFriendViewSet,
                       ProfileUsersViewSet,)


router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'profiles', ProfileViewSet, basename='profiles')
router_v1.register(r'profiles/(?P<profile_id>\d+)/friends',
                   GetDeleteFriendViewSet,
                   basename='friends')
router_v1.register(r'profiles/(?P<profile_id>\d+)/users',
                   ProfileUsersViewSet,
                   basename='profile_users')

auth_patterns = [
    path('signup/', SignUpViewSet.as_view())
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
