from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from products import urls as products_urls
from home import urls as home_urls
from users import urls as users_urls
from address import urls as addres_urls

#from Chat import urls as chat_urls
#from Chat.views import (    room)

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include(home_urls)),
    path('login/', auth_views.LoginView.as_view(),  name='login'),
    path('admin/', admin.site.urls),
    path('products/', include(products_urls)),
    path('users/', include(users_urls)),
    
    path('notifications/', include('notification.urls')),
    path('chat/', include('Chat.urls')),
    #path('chat/', include(chat_urls)),
    #path('chat/', room, name='room'),
    
    #reset password
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

    path('address/', include(addres_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



