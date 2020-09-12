from django.http import HttpResponse

from django.shortcuts import render, redirect, HttpResponseRedirect
from usuarios.models import Usuario 



def hello(request):
    return render(request, 'index.html')

    # Create your views here.
def index(request):
    if request.method == 'POST':
        usuarios = Usuario(usuario_nome=request.POST['usuario_nome'], usuario_senha=request.POST['usuario_senha'], usuario_email=request.POST['usuario_email'])
        usuarios.save()
        return redirect('/')
    else:
        return render(request, 'index.html')
 
def login(request):
    return render(request, 'login.html')
 
def home(request):
    return render(request, 'home.html')


def cadastro(request):
    return render(request, 'cadastro.html')

    #if request.method == 'POST':
     #   if Usuario.objects.filter(usuario_email=request.POST['usuario_email'], usuario_senha=request.POST['usuario_senha']).exists():
      #      usuarios = Usuario.objects.get(usuario_email=request.POST['usuario_email'], usuario_senha=request.POST['usuario_senha'])
       #     return render(request, 'home.html', {'usuarios': usuarios})
       # else:
       #     context = {'msg': 'Invalid email or password'}
       #     return render(request, 'login.html', context)