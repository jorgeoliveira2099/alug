from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from notification.models import Notification


def ShowNOtifications(request):
    user = request.user.id
    notifications1 = Notification.objects.filter(user=user,viewed=False)
    Notification.objects.filter(user=user, viewed=False)
    notifications = Notification.objects.all().filter(user=user, viewed=False)
   
    template = loader.get_template('notifications/notifications.html')

    context = {
        'notifications': notifications,
    }

    return HttpResponse(template.render(context, request))

def DeleteNotification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    noti_id = Notification.viewed = True
    return redirect('show_notifications')


def CountNotifications(request):
    user = request.user
    count_notifications = 0
    if request.user.is_authenticated:

        count_notifications = Notification.objects.filter(user=user, viewed=False).count()

    return {'count_notifications':count_notifications}
    

def MarkAllAsRead(request):
    user = request.user
    Notification.objects.all().filter(user=user).delete()
    return redirect('show_notifications')
