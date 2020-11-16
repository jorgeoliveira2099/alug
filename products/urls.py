from django.urls import path


from .views import (
    my_detail_product,
    lista_products,
    list_products,
    create_product,
    update_product,
    delete_product,
    detail_product,
    favourite_products,
    products_favourite_list,
    denunciar,
    alugar,
    alugarSubmit,
    produtosRequisitados,
    detalharAluguel,
    confirmarAluguel,
    encerrarAluguel,
    pesquisa,
    cancelarAluguel,
)


urlpatterns = [
    path('lista/', lista_products, name='lista_products'),
    path('list/<int:userId>/', list_products, name='list_products'),
    path('new/', create_product, name='create_products'),
    path('update/<int:productId>/', update_product, name='update_product'),
    path('delete/<int:productId>/', delete_product, name='delete_product'),
    path('denuncia/<int:productId>/', denunciar, name='denuncia'),
    path('alugar/<int:productId>/', alugar, name='alugar'),
     
    path('alugar/<int:productId>/submit', alugarSubmit, name='alugarSubmit'),
    path('detail/<int:id>/', detail_product, name='detail_product'),
    path('produtosRequisitados/', produtosRequisitados, name='produtos_requisitados'),
    path('detalharAluguel/<int:idAluguel>', detalharAluguel, name='detalhar_aluguel'),

    
    #url(r'(?P<id>\d+)/favourite_products/$', favourite_products, name='favourite_products'),
    path('detalharAluguel/<int:idAluguel>/confirmar', confirmarAluguel, name='confirmar_aluguel'),
    path('detalharAluguel/<int:idAluguel>/encerrar', encerrarAluguel, name='encerrar_aluguel'),
    
    path('cancelarAluguel/<int:idAluguel>/cancelar', cancelarAluguel, name='cancelar_aluguel'),
    #path('<int:id>/favourite_products/', favourite_products, name='favourite_products'),
    path('favourite_products/<int:id>/', favourite_products, name='favourite_products'),
  

    path('favoritos/', products_favourite_list, name='products_favourite_list'),
    
    path('mydetail/<int:productId>/', my_detail_product, name='my_detail_product'),

    path('favoritos/', products_favourite_list, name='products_favourite_list'),

    path('pesquisa/<slug:categoria>/', pesquisa, name='pesquisa'),
]
