from django.contrib import admin
from friends.models import User, FriendshipRequest, Profile

admin.site.register(User)
admin.site.register(FriendshipRequest)
admin.site.register(Profile)
