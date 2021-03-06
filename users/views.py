from django.shortcuts import render, redirect
from .admin import UserCreationForm
from django.urls import reverse_lazy
from .models import MyUser
from products.models import Product
from django.contrib.auth import authenticate
from django.contrib import messages
from address.models import Dados_usuario
from django.core.exceptions import ObjectDoesNotExist
from address.forms import Dados_usuarioForm
from django.db.models import Q

def register(request):
    form = UserCreationForm(request.POST or None)
    sucess_url = reverse_lazy('login')

    if form.is_valid():
        form.save()
        return redirect(sucess_url)

    return render(request, 'registration/register.html', {'form': form})

def excluirConta(request, userId):
    return render(request, 'user/excluir-usuario.html')

def excluirContaSubmit(request, userId):
    user = MyUser.objects.get(id=userId)
    excluir = 'excluir'
    senha = request.POST.get("senha")
    auth = authenticate(email=user.email, password=senha)

    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    form = Dados_usuarioForm(instance=perfil)


    if auth is not None:
       auth.delete()
       produtos = Product.objects.filter(Q(alugado=False)).order_by('-id')[0:8]
       context = {'products': produtos}
       messages.info(request, 'Sua conta foi excluída com sucesso!')
       return render(request, 'home/home.html', context)
    else:
       messages.error(request, 'Senha incorreta, favor informar a senha correta!')
    return render(request, 'user/perfil.html', {'form': form, 'perfil': perfil, 'excluir': excluir})
