from django.contrib import admin
from .models import Product, Categoria, Denuncia, Alugar, HistoricoStatus

admin.site.register(Categoria)
admin.site.register(Product)
admin.site.register(Denuncia)
admin.site.register(Alugar)
admin.site.register(HistoricoStatus)

