
from django.urls import path
from notification.views import ShowNOtifications, DeleteNotification


urlpatterns = [
    path('', ShowNOtifications, name='show_notifications'),
    path('<noti_id>/delete', DeleteNotification, name='delete_notification'),

]