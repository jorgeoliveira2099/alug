from django.urls import path
from .views import (
    list_products,
    create_product,
    update_product,
    delete_product
)


urlpatterns = [
    path('list/<int:userId>/', list_products, name='list_products'),
    path('new/<int:userId>/', create_product, name='create_products'),
    path('update/<int:productId>/', update_product, name='update_product'),
    path('delete/<int:productId>/', delete_product, name='delete_product'),
]
