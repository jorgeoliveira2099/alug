from django.contrib import admin
from django.urls import path, include
from .views import home, login, cadastro
from products.views import create_product, update_product, delete_product

app_name = 'products'

urlpatterns = [
	path('', login),
	path('login/', login),
	path('cadastro/', cadastro),
    path('admin/', admin.site.urls),
    path('home/', home),
	path('home/new', create_product, name='create_products'),
    path('home/update/<int:id>/', update_product, name='update_product'),
    path('home/delete/<int:id>/', delete_product, name='delete_product'),
    
]


