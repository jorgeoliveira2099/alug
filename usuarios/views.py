from django.shortcuts import render

def listar_usuarios(request):
	return render(request, 'index.html')
