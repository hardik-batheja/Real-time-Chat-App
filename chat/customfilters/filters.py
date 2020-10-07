from django import template

register = template.Library()

@register.filter('receivername')
def get_group_receiver(request):
    users=User.objects.filter(groups__name=self.name)
    if request.user.username == users[0].username:
        sender=users[0]
        receiver=user[1]
    else:
        sender=users[1]
        receiver=user[0]
    return receiver.username