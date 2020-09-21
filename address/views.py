from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.core.exceptions import ObjectDoesNotExist
from .forms import Dados_usuarioForm
from users.models import MyUser
from .models import Dados_usuario

def alterar_perfil(request,userId):
    user = MyUser.objects.get(id=userId)
    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()
    form = Dados_usuarioForm(request.POST or None, request.FILES or None, instance=perfil)
    perfil = form.save(commit=False)
    print(perfil.get_photo_url)
    if form.is_valid():
        dados_usuario = form.save(commit=False)
        dados_usuario.user = user
        dados_usuario.save()
        return redirect(reverse('perfil', kwargs={'userId': user.id}))

    return render(request, 'user/perfil.html', {'form': form, 'perfil': perfil})
