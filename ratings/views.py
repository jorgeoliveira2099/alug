from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render

from ratings.models import RatingForm, Rating, HistoricoAlugados
from users.models import MyUser


def avalia(request, idAvalia):
    user = request.user
    try:
        historico = HistoricoAlugados.objects.get(id=idAvalia)
    except ObjectDoesNotExist:
        return render(request, 'home/termosdeuso.html')
    
    usuario = ''
    alguem = 0
    if user == historico.locador:  
                              
        if historico.avaliadoPeloLocador == False:
            usuario = historico.locatario 
            alguem = 1           
    if user == historico.locatario:              
                
        if historico.avaliadoPeloLocatario == False:
            usuario = historico.locador
            alguem = 1              

    if alguem == 0:
        return render(request, 'home/termosdeuso.html')    

    context = {
        'historico':historico,
        'idAvalia':idAvalia,
        'usuario':usuario,
    }
    return render(request, 'user/avaliar.html', context)

def avaliarSubmit(request, idAvalia):
    url = request.META.get('HTTP_REFERER')
    user = request.user
    try:
        historico = HistoricoAlugados.objects.get(id=idAvalia)
    except ObjectDoesNotExist:
        return render(request, 'home/termosdeuso.html')

    usuario = ''
    locadorUser = ''
    locatarioUser = ''
    if user == historico.locador:
        historico.avaliadoPeloLocador = True
        historico.save()
        usuario = historico.locatario
    if user == historico.locatario:
        historico.avaliadoPeloLocatario = True
        historico.save()
        usuario = historico.locador

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():            
            data = Rating()             
            data.de = user
            data.para = usuario
            data.text = form.cleaned_data['text']
            data.rate = form.cleaned_data['rate']
            data.save()           
            messages.info(request, 'Agradecemos a sua avaliação!')

    user = request.user
    avaliacoes = HistoricoAlugados.objects.filter(Q(locador=user) | Q(locatario=user) & Q(encerrado=True))
    arrayPendentes = []
    for avaliacao in avaliacoes:
        if user == avaliacao.locador:

            if avaliacao.avaliadoPeloLocador == False:
                arrayPendentes.append(avaliacao)
        if user == avaliacao.locatario:

            if avaliacao.avaliadoPeloLocatario == False:
                arrayPendentes.append(avaliacao)

    return render(request, 'user/avaliacoesPendentes.html', {'avaliacoes': arrayPendentes})


def avaliacoesPendentes(request):
    user = request.user
    avaliacoes = HistoricoAlugados.objects.filter(Q(locador=user)| Q(locatario=user) & Q(encerrado=True))
    arrayPendentes = []
    for avaliacao in avaliacoes:
        if user == avaliacao.locador:  
                              
            if avaliacao.avaliadoPeloLocador == False:
                arrayPendentes.append(avaliacao)
        if user == avaliacao.locatario:

            if avaliacao.avaliadoPeloLocatario == False:
                arrayPendentes.append(avaliacao)

    return render(request, 'user/avaliacoesPendentes.html', {'avaliacoes': arrayPendentes})



def avaliacoesUsuario(request, idUsuario):
    user = request.user
    avaliacoes = Rating.objects.all().filter(Q(para=idUsuario))
    soma = 0
    
    
    num = avaliacoes.count()
    media = 0
    if num > 0:
        for avaliacao in avaliacoes:
            soma += avaliacao.rate    
        media = int(soma/num)

    usuario = MyUser.objects.get(id=idUsuario)

    context = {
               'avaliacoes': avaliacoes, 
               'soma':soma, 
               'media':media, 
               'usuario':usuario, 
               'num':num,                
            }
    return render(request, 'user/avaliacoesUsuario.html', context)

