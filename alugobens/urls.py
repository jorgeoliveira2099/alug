from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from products import urls as products_urls
from home import urls as home_urls
from users import urls as users_urls
from address import urls as addres_urls


urlpatterns = [
    path('', include(home_urls)),
    path('login/', auth_views.LoginView.as_view(),  name='login'),
    path('admin/', admin.site.urls),
    path('products/', include(products_urls)),
    path('users/', include(users_urls)),
    path('address/', include(addres_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


