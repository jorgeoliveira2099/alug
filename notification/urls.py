
from django.urls import path
from notification.views import ShowNOtifications, DeleteNotification, MarkAllAsRead


urlpatterns = [
    path('', ShowNOtifications, name='show_notifications'),
    path('<noti_id>/delete', DeleteNotification, name='delete_notification'),
    path('delete', MarkAllAsRead, name='markall_as_read'),

]