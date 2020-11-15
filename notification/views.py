from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from notification.models import Notification
# Create your views here.

def ShowNOtifications(request):
    user = request.user.id
    #isso é o usuario logado
    print(user)
    print('aaaaaaaaaaaaaaaquiiiiiiiiiiiiii')
    notifications1 = Notification.objects.filter(user=user,viewed=False)
    Notification.objects.filter(user=user, viewed=False)
    #aqui funciona
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
     #   count_notifications = Notification.objects.filter(user=request.user, viewed=False).count()
   
        count_notifications = Notification.objects.filter(user=user, viewed=False).count()

    return {'count_notifications':count_notifications}
    

def MarkAllAsRead(request):
    user = request.user
    Notification.objects.all().filter(user=user).delete()
    #contador = Notification.objects.all().filter(user=user).count()
    #print(contador)
    #print('NUMERO DE NOTIFICAÇOES')
    return redirect('show_notifications')
