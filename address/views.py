from django.shortcuts import render, redirect
from .admin import DadosUsuarioCreateForm
from .models import Dados_usuario

from django.urls import reverse_lazy

def perfil(request):
    form = DadosUsuarioCreateForm(request.POST or None)
    sucess_url = reverse_lazy('perfil')

    user = request.user

    
    print(user)

    if form.is_valid():
        form.save()
        return redirect(sucess_url)

    return render(request, 'user/perfil.html', {'form': form})