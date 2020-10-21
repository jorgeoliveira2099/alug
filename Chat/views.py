from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from Chat.models import Chat
from Chat.models import Mensagem
from django.db.models import Q
from alugobens.util import gerarHash
from users.models import MyUser
from address.models import Dados_usuario

def criarSala(request, idLocatario, idLocador):
    user = MyUser.objects.get(id=idLocador)
    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    try:
        chat = Chat.objects.get(locador=idLocador, locatario=idLocatario)
    except ObjectDoesNotExist:
        chat = Chat()
        chat.codigoSala = gerarHash(50)
        chat.locatario = idLocatario
        chat.locador = idLocador
        chat.save()

    if perfil.nome == None or perfil.sobrenome == None:
        identificador = user.email
    else:
        identificador = perfil.nome + " " + perfil.sobrenome

    mensagensChat = chat.mensagem_set.all()
    mensagens = ''

    for mensagemChat in mensagensChat:
        mensagens += mensagemChat.texto + "\n"

    return render(request, 'chat/chat.html',
                  {'room_name': chat.codigoSala, 'identificador': identificador, 'mensagems': mensagens})


def criarSalaSubmit(request, idLocatario, idLocador):
    mensagemEnviada = request.POST.get("mensagem")

    user = MyUser.objects.get(id=idLocador)
    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    if perfil.nome == None or perfil.sobrenome == None:
        identificador = user.email
    else:
        identificador = perfil.nome + " " + perfil.sobrenome

    chat = Chat.objects.get(locador=idLocador, locatario=idLocatario)
    mensagem = Mensagem()
    mensagem.texto = identificador + ": " + mensagemEnviada
    mensagem.chat = chat
    mensagem.save()

    mensagensChat = chat.mensagem_set.all()
    mensagens = ''

    for mensagemChat in mensagensChat:
        mensagens += mensagemChat.texto + "\n"

    return render(request, 'chat/chat.html',
                  {'room_name': chat.codigoSala, 'identificador': identificador, 'mensagems': mensagens})

def room(request, room_name, userId):
    user = MyUser.objects.get(id=userId)
    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    try:
        chat = Chat.objects.get(codigoSala=room_name)
    except ObjectDoesNotExist:
        return render(request, 'home/home.html')

    if perfil.nome == None or perfil.sobrenome == None:
        identificador = user.email
    else:
        identificador = perfil.nome + " " + perfil.sobrenome

    if chat.locatario == str(userId) or chat.locador == str(userId):
        mensagensChat = chat.mensagem_set.all()
        mensagens = ''

        for mensagemChat in mensagensChat:
            mensagens += mensagemChat.texto + "\n"

        return render(request, 'chat/chat.html',
                      {'room_name': chat.codigoSala, 'identificador': identificador, 'mensagems': mensagens})

    return render(request, 'home/home.html')

def roomSubmit(request, room_name, userId):
    user = MyUser.objects.get(id=userId)
    mensagemEnviada = request.POST.get("mensagem")
    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    if perfil.nome == None or perfil.sobrenome == None:
        identificador = user.email
    else:
        identificador = perfil.nome + " " + perfil.sobrenome

    chat = Chat.objects.get(codigoSala=room_name)
    mensagem = Mensagem()
    mensagem.texto = identificador + ": " + mensagemEnviada
    mensagem.chat = chat
    mensagem.save()

    mensagensChat = chat.mensagem_set.all()
    mensagens = ''

    for mensagemChat in mensagensChat:
        mensagens += mensagemChat.texto + "\n"

    return render(request, 'chat/chat.html',
                  {'room_name': chat.codigoSala, 'identificador': identificador, 'mensagems': mensagens})

def meusChats(request):
    user = request.user
    chats = Chat.objects.filter((Q(locador=user.id) | Q(locatario=user.id)))

    for chat in chats:
        if chat.locador != str(user.id):
            user = MyUser.objects.get(id=chat.locador)
            try:
                perfil = Dados_usuario.objects.get(user=user)
            except ObjectDoesNotExist:
                perfil = Dados_usuario()

            if perfil.nome == None or perfil.sobrenome == None:
                identificador = user.email
            else:
                identificador = perfil.nome + " " + perfil.sobrenome
            chat.nomeSala = "Chat com " + identificador
        elif chat.locatario != str(user.id):
            user = MyUser.objects.get(id=chat.locatario)
            try:
                perfil = Dados_usuario.objects.get(user=user)
            except ObjectDoesNotExist:
                perfil = Dados_usuario()

            if perfil.nome == None or perfil.sobrenome == None:
                identificador = user.email
            else:
                identificador = perfil.nome + " " + perfil.sobrenome
            chat.nomeSala = "Chat com " + identificador




    return render(request, 'chat/meus-chats.html', {'chats': chats})



