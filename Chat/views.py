from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
# teste
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse_lazy
from xhtml2pdf import pisa

from Chat.models import Chat
from Chat.models import Mensagem
from address.models import Dados_usuario
from alugobens.util import gerarHash
from products.models import Alugar
from products.models import Product
from ratings.models import HistoricoAlugados


@login_required
def criarSala(request, idProduto):
    user = request.user
    produto = Product.objects.get(id=idProduto)
    locador = produto.user
    if user == produto.user:
        return render(request, 'paginaErro.html')
    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    try:
        chat = Chat.objects.get(locatario=user, locador=locador, produto=produto)
    except ObjectDoesNotExist:
        chat = Chat()
        chat.codigoSala = gerarHash(20)
        chat.locatario = user
        chat.locador = locador
        chat.produto = produto
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
                  {
                    'room_name': chat.codigoSala,
                    'identificador': identificador,
                    'mensagems': mensagens,
                    'produto': produto,
                    'desabilitarAlugar': existeAluguelEmAndamento(produto)})


@login_required
def criarSalaSubmit(request, idProduto):
    mensagemEnviada = request.POST.get("mensagem")
    user = request.user
    produto = Product.objects.get(id=idProduto)
    locador = produto.user

    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    if perfil.nome == None or perfil.sobrenome == None:
        identificador = user.email
    else:
        identificador = perfil.nome + " " + perfil.sobrenome

    chat = Chat.objects.get(locador=locador, locatario=user, produto=produto)
    mensagem = Mensagem()
    mensagem.texto = identificador + ": " + mensagemEnviada
    mensagem.chat = chat
    mensagem.user = locador
    mensagem.save()

    mensagensChat = chat.mensagem_set.all()
    mensagens = ''

    for mensagemChat in mensagensChat:
        mensagens += mensagemChat.texto + "\n"

    return render(request, 'chat/chat.html',
                  {'room_name': chat.codigoSala, 'identificador': identificador,
                   'mensagems': mensagens, 'produto': produto,
                    'desabilitarAlugar': existeAluguelEmAndamento(produto)})

@login_required
def room(request, room_name):
    user = request.user

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

    if chat.locatario == user or chat.locador == user:
        mensagensChat = chat.mensagem_set.all()
        mensagens = ''

        for mensagemChat in mensagensChat:
            mensagens += mensagemChat.texto + "\n"

        return render(request, 'chat/chat.html',
                      {'room_name': chat.codigoSala, 'identificador': identificador,
                       'mensagems': mensagens, 'produto': chat.produto,
                       'desabilitarAlugar': existeAluguelEmAndamento(chat.produto)})

    return render(request, 'home/home.html')

@login_required
def roomSubmit(request, room_name):
    user = request.user
    try:
        chat = Chat.objects.get(codigoSala=room_name)
    except ObjectDoesNotExist:
        return render(request, 'home/home.html')

    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    if perfil.nome == None or perfil.sobrenome == None:
        identificador = user.email
    else:
        identificador = perfil.nome + " " + perfil.sobrenome

    if user != chat.locatario:
        usuarioNotificacao = chat.locatario
    else:
        usuarioNotificacao = chat.locador

    mensagemEnviada = request.POST.get("mensagem")
    mensagem = Mensagem()
    mensagem.texto = identificador + ": " + mensagemEnviada
    mensagem.chat = chat
    mensagem.user = usuarioNotificacao
    mensagem.save()

    mensagensChat = chat.mensagem_set.all()
    mensagens = ''

    for mensagemChat in mensagensChat:
        mensagens += mensagemChat.texto + "\n"

    return render(request, 'chat/chat.html',
                  {'room_name': chat.codigoSala, 'identificador': identificador,
                   'mensagems': mensagens, 'produto': chat.produto,
                   'desabilitarAlugar': existeAluguelEmAndamento(chat.produto)})

@login_required
def meusChats(request):
    user = request.user
    chats = Chat.objects.filter((Q(locador=user) | Q(locatario=user)))

    for chat in chats:
        if chat.locador != user:
            try:
                perfil = Dados_usuario.objects.get(user=chat.locador)
            except ObjectDoesNotExist:
                perfil = Dados_usuario()

            if perfil.nome == None or perfil.sobrenome == None:
                identificador = chat.locador.email
            else:
                identificador = perfil.nome + " " + perfil.sobrenome
            chat.nomeSala = identificador
        elif chat.locatario != user:

            try:
                perfil = Dados_usuario.objects.get(user=chat.locatario)
            except ObjectDoesNotExist:
                perfil = Dados_usuario()

            if perfil.nome == None or perfil.sobrenome == None:
                identificador = chat.locatario.email
            else:
                identificador = perfil.nome + " " + perfil.sobrenome
            chat.nomeSala = identificador

    return render(request, 'chat/meus-chats.html', {'chats': chats})


@login_required
def exportarpdf(request, room_name):
    user = request.user

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

    if chat.locatario == user or chat.locador == user:
        mensagensChat = chat.mensagem_set.all()
        mensagens = ''

        for mensagemChat in mensagensChat:
            mensagens += mensagemChat.texto + "\n"


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

def existeAluguelEmAndamento(produto):

    try:
       aluguel = Alugar.objects.get(produto=produto)
       return True
    except ObjectDoesNotExist:
        pass

    historicos = HistoricoAlugados.objects.filter((Q(produto=produto)))

    for historico in historicos:
        if not historico.encerrado:
            return True

    return False