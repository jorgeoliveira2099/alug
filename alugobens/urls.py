from django.contrib import admin
from django.urls import path, include
from products import urls as products_urls
from home import urls as home_urls
from users import urls as users_urls
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include(home_urls)),
    path('login/', auth_views.LoginView.as_view(),  name='login'),
    path('admin/', admin.site.urls),
    path('products/', include(products_urls)),
    path('users/', include(users_urls)),
]


