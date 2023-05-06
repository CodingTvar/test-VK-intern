from django.contrib import admin
from friends.models import User, FriendshipRequest

admin.site.register(User)
admin.site.register(FriendshipRequest)
