import django_filters

from .models import Product, Categoria

def categories(request):
    if request is None:
        return Categoria.objects.none()

    category = request.Categoria.objects.all()
    
    return Categoria.objects.all()

class FilterCategory(django_filters.FilterSet):
    

    nome = django_filters.CharFilter(lookup_expr='icontains')
    #categoria = django_filters.ModelChoiceFilter(queryset=categories)
   

    class Meta:
        model = Product
        fields = ('nome', 'categoria')
