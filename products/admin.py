from django.contrib import admin
from .models import Product, Categoria, Denuncia

admin.site.register(Categoria)
admin.site.register(Product)
admin.site.register(Denuncia)


