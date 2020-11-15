from django.shortcuts import render

from django.shortcuts import render, redirect, HttpResponseRedirect,HttpResponse
from ratings.models import RatingForm, Rating, HistoricoAlugados
from django.contrib import messages
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet
#def avaliacoesPendentes(request):   
 #   return render(request, 'user/avaliacoesPendentes.html')
from users.models import MyUser

def avalia(request, idAvalia):
    user = request.user
    #posso usar isso
    #historico = HistoricoAlugados.objects.filter(Q(locador=user)| Q(locatario=user) & Q(encerrado=True))#.first()
    #h = historico.id
    #print(h)
    try:
        #AQUI EU TO VERIFICANDO SE EXISTE UM HISTORICO COM ESTE ID
        #historico = HistoricoAlugados.objects.filter(Q(locador=user)| Q(locatario=user) & Q(encerrado=True) & Q(id=idAvalia))#.first()
        #eu posso usar isso ainda, pode ser util
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
        print('ENTROU AQUIIIIIIII É LOCATARIO')
        
    if alguem == 0:
        return render(request, 'home/termosdeuso.html')    

    #aqui para baixo é lixo
    #historicoAluga = HistoricoAlugados.objects.get(id=h)
    #aqui eu posso verificar se o usuario logado está 
    #em algum objeto de avaliação, se ele estiver, não exibe
#aqui é o apenas o método para renderizar o formulário de avaliação    
    context = {
        'historico':historico,
        'idAvalia':idAvalia,
        'usuario':usuario,
    }
    return render(request, 'user/avaliar.html', context)

#aqui o metodo que pera a requisição do formulário
#AVALIAR SUBMIT
def avaliarSubmit(request, idAvalia):
    url = request.META.get('HTTP_REFERER')
    print('USUARIO AQUIIIIIIIII')
    user = request.user
    print('USUARIO AQUIIIIIIIII')
    print(user)
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
        print('SALVOUUUUUUUUUUUUUU')
        print(historico.avaliadoPeloLocador)
        usuario = historico.locatario
            #usuario = historico.locatario            
    if user == historico.locatario: 
        historico.avaliadoPeloLocatario = True
        historico.save()
        usuario = historico.locador
            #usuario = historico.locador             
        


    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():            
            data = Rating()             
            data.de = user
            data.para = usuario
            data.text = form.cleaned_data['text']
            data.rate = form.cleaned_data['rate']
            data.save()           
            print('SALVOUUUUUUUUUUUUUU')
            messages.info(request, 'Usuario avaliado com sucesso!')
              #  return HttpResponseRedirect(url)
            context = {
                #'historico':historico,
                'idAvalia':idAvalia,
                #'usuario':usuario,
            }
       
    return render(request, 'home/termosdeuso.html', context)
    #return HttpResponse('comentario adicionado')
#return HttpResponseRedirect(url)


def avaliacoesPendentes(request):
    user = request.user
    avaliacoes = HistoricoAlugados.objects.filter(Q(locador=user)| Q(locatario=user) & Q(encerrado=True))
    arrayPendentes = []
    for avaliacao in avaliacoes:
        if user == avaliacao.locador:  
                              
            if avaliacao.avaliadoPeloLocador == False:
                arrayPendentes.append(avaliacao)
                print(arrayPendentes)
        if user == avaliacao.locatario:              
            
            if avaliacao.avaliadoPeloLocatario == False:
                arrayPendentes.append(avaliacao)
                print(arrayPendentes)
            print('ENTROU AQUIIIIIIII É LOCATARIO')

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

