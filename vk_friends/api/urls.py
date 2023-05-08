from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (SignUpView,
                       UserViewSet,
                       ProfileViewSet,
                       FriendshipRequestViewSet)


router_v1 = DefaultRouter()
# router_v1.register(r'profiles', ProfileViewSet, basename='profiles')
router_v1.register(r'users', UserViewSet, basename='users')
#router_v1.register(r'friendships_request',
#                   FriendshipRequestViewSet,
#                   basename='friendships_request')

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/', include(router_v1.urls)),
]
