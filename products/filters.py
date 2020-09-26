import django_filters

from .models import *

class FilterCategory(django_filters.FilterSet):
	class Meta:
		model = Categoria
		fields = '__all__'