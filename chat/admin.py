from django.contrib import admin

from .models import *

admin.site.register(Message)
class ChatGroupAdmin(admin.ModelAdmin):
    """ enable Chart Group admin """
    list_display = ('id', 'name', 'description', 'icon', 'mute_notifications', 'date_created', 'date_modified')
    list_filter = ('id', 'name', 'description', 'icon', 'mute_notifications', 'date_created', 'date_modified')
    list_display_links = ('name',)

admin.site.register(ChatGroup, ChatGroupAdmin)
class ProfileAdmin(admin.ModelAdmin):
    """ enable Chart Group admin """
    list_display = ('id', 'user','status')
    list_filter = ('id', 'user','status')

admin.site.register(UserProfile,ProfileAdmin)

