from django.shortcuts import render

from django.shortcuts import render, redirect, HttpResponseRedirect,HttpResponse
from ratings.models import RatingForm, Rating, HistoricoAlugados
from django.contrib import messages
from django.db.models import Q

#def avaliacoesPendentes(request):   
 #   return render(request, 'user/avaliacoesPendentes.html')


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
    
    
    
    
    #historico = HistoricoAlugados.objects.filter(Q(locador=user)| Q(locatario=user) & Q(encerrado=True))#.first()
    
    # esse quaase funciona
    #historico = HistoricoAlugados.objects.filter(Q(locador=user)| Q(locatario=user) & Q(encerrado=True) | ~(Q(avaliadoPeloLocador=False) & Q(avaliadoPeloLocatario=False)))
    
    #h = historico.id
    #avaliadoPeloLocador
    #avaliadoPeloLocatario
    # if user == historico.locador, ele faz algo
    #historicoAluga = HistoricoAlugados.objects.get(id=h)
    #excluir aui ?
    #historicoAluga = HistoricoAlugados.objects.get(id=h)
    #a = historico.values()
    print('ENTROU AQUIIIIIIII É O IDDDDDDDDDDDDDDDDDDDDDDD')
    #print(historicoAluga)
    #print(historicoAluga)

    print('ENTROU AQUIIIIIIII É IDDDDDDDDDDDDDDDDDDDDDDD')
    #muito provavelmente eu vou precisar disso
    #avaliacoes = Rating.objects.filter(Q(locador=user)| Q(locatario=user))
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
        

    #usuario = ''
   # locadorUser = ''
    #locatarioUser = ''
    #if user == historico.locador:
       #if historico.avaliadoPeloLocador == False:
       # usuario = historico.locatario 
            #usuarioDe = historicoAluga.locador
            #usuarioPara = historicoAluga.locatario

       # historicoAluga.avaliadoPeloLocador = True
      #  historicoAluga.save()
        
     #   print('ENTROU AQUIIIIIIII É LOCADOR')

    #if user == historicoAluga.locatario:
    #else:
        #está dando um bug aqui, ele sempre joga o admim aqui
        #usuarioDe = historicoAluga.locatario
        #usuarioPara = historicoAluga.locador

        #historicoAluga.avaliadoPeloLocatario = True
        #historicoAluga.save()
        #print('ENTROU AQUIIIIIIII É LOCATARIO')

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



    #user = request.user   
    #historico = HistoricoAlugados.objects.all()filter(Q(locador=user)| Q(locatario=user) & Q(encerrado=True))
       
    #for h in historico:
     #   if user == h.locador:                   
      #      print('ENTROU AQUIIIIIIII É LOCADOR')
       # if user == h.locatario:        
        #    print('ENTROU AQUIIIIIIII É LOCATARIO')