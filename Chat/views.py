from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from Chat.models import Chat
from alugobens.util import gerarHash
from users.models import MyUser
from products.models import Product
from address.models import Dados_usuario



def index(request):
    #title: 'Meu chat'
    return render(request, 'main.html', {})

def criarSala(request, idLocatario, idLocador, idProduto):
    produto = Product.objects.get(id=idProduto)
    identificador = ''

    user = MyUser.objects.get(id=idLocador)
    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    try:
        chat = Chat.objects.get(locador=idLocador, locatario=idLocatario, produto=produto)
    except ObjectDoesNotExist:
        chat = Chat()
        chat.codigoSala = gerarHash(50)
        chat.locatario = idLocatario
        chat.locador = idLocador
        chat.produto = produto
        chat.save()

    if perfil.nome == None or perfil.sobrenome == None:
        identificador = user.email
    else:
        identificador = perfil.nome + " " + perfil.sobrenome

    return render(request, 'chat.html', {'room_name': chat.codigoSala, 'identificador': identificador})


def room(request, room_name, userId):
    chat = Chat.objects.get(codigoSala=room_name)

    if chat.locatario == userId or chat.locatario == userId:
        return render(request, 'chat.html', {
            'room_name': room_name
        })

    return render(request, 'home/home.html')

