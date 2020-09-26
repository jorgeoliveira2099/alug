from django.shortcuts import render, redirect
from .admin import UserCreationForm
from django.urls import reverse_lazy
from .models import MyUser
from django.contrib.auth import authenticate
from django.contrib import messages

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

    senha = request.POST.get("senha")
    auth = authenticate(email=user.email, password=senha)
    if auth is not None:
       auth.delete()
       messages.info(request, 'Usuario excluido com sucesso!')
       return render(request, 'home/home.html')
    else:
       messages.error(request, 'Senha incorreta, favor informar a senha correta!')
    return render(request, 'user/excluir-usuario.html')
