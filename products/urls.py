from django.urls import path
from .views import (
    my_detail_product,
    lista_products,
    list_products,
    create_product,
    update_product,
    delete_product,
    detail_product
)


urlpatterns = [
    path('lista/', lista_products, name='lista_products'),
    path('list/<int:userId>/', list_products, name='list_products'),
    path('new/<int:userId>/', create_product, name='create_products'),
    path('update/<int:productId>/', update_product, name='update_product'),
    path('delete/<int:productId>/', delete_product, name='delete_product'),
    path('detail/<int:productId>/', detail_product, name='detail_product'),
    path('mydetail/<int:productId>/', my_detail_product, name='my_detail_product'),
]
