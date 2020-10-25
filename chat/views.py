from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver    


import json

def index(request):
    return render(request, 'chat/index.html', {})
def get_participants(group_id=None, group_obj=None, user=None):
    """ function to get all participants that belong the specific group """
    
    if group_id:
        chatgroup = ChatGroup.objects.get(id=id)
    else:
        chatgroup = group_obj

    temp_participants = []
    for participants in chatgroup.user_set.values_list('username', flat=True):
        if participants != user:
            temp_participants.append(participants.title())
    temp_participants.append('You')
    return ', '.join(temp_participants)


@login_required
def room(request, group_id):
    if request.user.groups.filter(id=group_id).exists():
        chatgroup = ChatGroup.objects.get(id=group_id)
        users=User.objects.filter(groups__name=chatgroup.name)
        if request.user.username == users[0].username:
            sender=users[0]
            receiver=users[1]
        else:
            sender=users[1]
            receiver=users[0]

        print(chatgroup)
        #TODO: make sure user assigned to existing group
        assigned_groups = list(request.user.groups.values_list('id', flat=True))
        print(assigned_groups)
        groups_participated = ChatGroup.objects.filter(id__in=assigned_groups)
        print(groups_participated)
        return render(request, 'chat/room.html', {
            'chatgroup': chatgroup,
            'participants': get_participants(group_obj=chatgroup, user=request.user.username),
            'groups_participated': groups_participated,
            'sender':sender,
            'receiver':receiver
        })
    else:
        return HttpResponseRedirect("unauthorized")

# @receiver(user_logged_in)
# def got_online(sender, user, request, **kwargs):    
#     user.profile.is_online = True
#     user.profile.save()

# @receiver(user_logged_out)
# def got_offline(sender, user, request, **kwargs):   
#     user.profile.is_online = False
#     user.profile.save()

# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name_json': mark_safe(json.dumps(room_name)),
#         'username': mark_safe(json.dumps(request.user.username)),
#     })
