from django.contrib import admin
from django.urls import path, include
from .views import home, login, cadastro
from usuarios import urls as usuarios_urls


urlpatterns = [
	path('/', login),
	path('login/', login),
	path('cadastro/', cadastro),
    path('admin/', admin.site.urls),
    path('usuario/', include(usuarios_urls)),

    path('home/', home),
    
]


