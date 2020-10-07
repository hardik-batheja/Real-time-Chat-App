from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import Group
from chat.middileware import RequestMiddleware


User = get_user_model()
class ChatGroup(Group):
    """ extend Group model to add extra info"""
    description = models.TextField(blank=True, help_text="description of the group")
    mute_notifications = models.BooleanField(default=False, help_text="disable notification if true")
    icon = models.ImageField(help_text="Group icon", blank=True, upload_to="chartgroup")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('chat:room', args=[str(self.id)])
    def get_group_receiver(self):
        users=User.objects.filter(groups__name=self.name)
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request

        if request.user.username == users[0].username:
            sender=users[0]
            receiver=users[1]
        else:
            sender=users[1]
            receiver=users[0]
        return receiver.username

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chatgroup=models.ForeignKey(ChatGroup,on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username

    def last_10_messages(self):
        
        return Message.objects.filter(chatgroup=self).order_by('timestamp')