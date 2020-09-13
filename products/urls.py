from django.urls import path
from .views import login, cadastro, home, list_products, create_product, update_product, delete_product


urlpatterns = [
	path('', login, name='login'),
    path('home', list_products, name='list_products'),
    path('cadastro', cadastro, name='cadastro'),
    path('home/new', create_product, name='create_products'),
    path('home/update/<int:id>/', update_product, name='update_product'),
    path('home/delete/<int:id>/', delete_product, name='delete_product'),
]
