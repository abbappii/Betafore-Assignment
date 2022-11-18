from django.contrib import admin

# Register your models here.

from friend.models import FriendList, FriendRequests

class FriendListAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList

admin.site.register(FriendList, FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender','receiver']
    list_display = ['sender','receiver']
    search_fields = ['sender__username','sender__email','receiver__email','receiver__ username']

    class Meta:
        model = FriendRequests

admin.site.register(FriendRequests, FriendRequestAdmin)



