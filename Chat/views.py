from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from Chat.models import Chat
from Chat.models import Mensagem
from django.db.models import Q
from alugobens.util import gerarHash
from users.models import MyUser
from address.models import Dados_usuario

#teste
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.urls import reverse_lazy

def criarSala(request, idLocatario, idLocador):
    user = MyUser.objects.get(id=idLocador)
    locador = MyUser.objects.get(id=idLocador)
    products = locador.product_set.all()
    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    try:
        chat = Chat.objects.get(locador=idLocador, locatario=idLocatario)
    except ObjectDoesNotExist:
        chat = Chat()
        chat.codigoSala = gerarHash(20)
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
                  {'room_name': chat.codigoSala, 'identificador': identificador,
                   'mensagems': mensagens, 'products': products})


def criarSalaSubmit(request, idLocatario, idLocador):
    mensagemEnviada = request.POST.get("mensagem")
    usuarioLocatario = MyUser.objects.get(id=idLocatario)
    user = MyUser.objects.get(id=idLocador)

    locador = MyUser.objects.get(id=idLocador)
    products = locador.product_set.all()

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
    mensagem.user = usuarioLocatario
    mensagem.save()

    mensagensChat = chat.mensagem_set.all()
    mensagens = ''

    for mensagemChat in mensagensChat:
        mensagens += mensagemChat.texto + "\n"

    return render(request, 'chat/chat.html',
                  {'room_name': chat.codigoSala, 'identificador': identificador,
                   'mensagems': mensagens, 'products': products})

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

    print(chat.locador)
    print(userId)
    if chat.locador != str(userId):
        print('entrou')
        locador = MyUser.objects.get(id=chat.locador)
        products = locador.product_set.all()
        print(products)
    else:
        products = []

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
                      {'room_name': chat.codigoSala, 'identificador': identificador,
                       'mensagems': mensagens, 'products': products})

    return render(request, 'home/home.html')

def roomSubmit(request, room_name, userId):
    user = MyUser.objects.get(id=userId)
    
    #inicia aqui
     #aqui
    #user = request.user
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
            #chat.nomeSala = "Chat com " + identificador
            usuarioLocatario = identificador
        elif chat.locatario != str(user.id):
            user = MyUser.objects.get(id=chat.locatario)
            try:
                perfil = Dados_usuario.objects.get(user=user)
            except ObjectDoesNotExist:
                perfil = Dados_usuario()

            if perfil.nome == None or perfil.sobrenome == None:
                identificador = user.email
                usuarioLocatario = identificador
            else:
                identificador = perfil.nome + " " + perfil.sobrenome
            usuarioLocatario = identificador
    #aqui
    #termina aqui

    usuarioo = MyUser.objects.get(email=usuarioLocatario)
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
    mensagem.user = usuarioo
    mensagem.save()

    mensagensChat = chat.mensagem_set.all()
    mensagens = ''

    print(chat.locador)
    print(userId)
    if chat.locador != str(userId):
        print('entrou')
        locador = MyUser.objects.get(id=chat.locador)
        products = locador.product_set.all()
    else:
        products = []

    for mensagemChat in mensagensChat:
        mensagens += mensagemChat.texto + "\n"

    return render(request, 'chat/chat.html',
                  {'room_name': chat.codigoSala, 'identificador': identificador,
                   'mensagems': mensagens, 'products': products})

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



def exportarpdf(request, room_name, userId):
    user = MyUser.objects.get(id=userId)
    chat = Chat.objects.get(codigoSala=room_name)
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

    #ddaqui para baixo funciona
    
    usuario = 1
    try:
        template = get_template('chat/chat2.html')
        context = {'mensagems': mensagens, 'room_name': chat.codigoSala, 'user.id': user.id,'title': 'chhat'}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="chat.pdf"'
        pisaStatus = pisa.CreatePDF(html, dest=response)

        return response
    except:
        pass
    return HttpResponseRedirect(reverse_lazy('meusChats'))
    #user = MyUser.objects.get(id=userId)
    #try:
     #   perfil = Dados_usuario.objects.get(user=user)
    #except ObjectDoesNotExist:
     #   perfil = Dados_usuario()

    #try:
     #   chat = Chat.objects.get(codigoSala=room_name)
    #except ObjectDoesNotExist:
     #   return render(request, 'home/home.html')

  #  if perfil.nome == None or perfil.sobrenome == None:
     #   identificador = user.email
   # else:
   #     identificador = perfil.nome + " " + perfil.sobrenome

   # if chat.locatario == str(userId) or chat.locador == str(userId):
     #   mensagensChat = chat.mensagem_set.all()
      #  mensagens = ''

     #   for mensagemChat in mensagensChat:
        #    mensagens += mensagemChat.texto + "\n"

     #   return render(request, 'chat/chat.html',
        #              {'room_name': chat.codigoSala, 'identificador': identificador, 'mensagems': mensagens})

   # return render(request, 'home/home.html')

