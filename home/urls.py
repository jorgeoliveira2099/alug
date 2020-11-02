from django.urls import path
from .views import home, my_logout
from products.views import lista_products

urlpatterns = [
    path('', lista_products, name='home'),
    path('logout/', my_logout, name='logout'),
]