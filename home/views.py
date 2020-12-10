from django.shortcuts import render, redirect
from django.contrib.auth import logout
from products.models import Product, Categoria
from address.models import Dados_usuario
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    produtos = Product.objects.filter(Q(alugado=False)).order_by('-id')[0:8]
    context = {'products': produtos}
    gerarCategorias()

    return render(request, 'home/home.html', context)

def my_logout(request):
    logout(request)
    return redirect('home')

def termosDeUso(request):
    return render(request, 'home/termosdeuso.html')

def perguntasFrequentes(request):
    return render(request, 'home/perguntasfrequentes.html')

def sejaPrime(request):
    return render(request, 'home/sejaPrime.html')

def politicaCookies(request):
    return render(request, 'home/politicaCookies.html')

def pesquisa(request):
    categoria = request.POST.get('categoria')
    resposta = request.GET.get('page')
    nome = request.POST.get('nome')
    estado = request.POST.get('estado')

    cidade = request.POST.get('cidade')
    if resposta != None:
        respostas = resposta.split("_")
        page = respostas[0]
        nomeGET = respostas[1]
        estado = respostas[2] if respostas[2] != 'None' else ''
        cidade = respostas[3] if respostas[3] != 'None' else ''
        categoria = respostas[4] if respostas[4] != 'None' else ''
    else:
        page = None
        nomeGET = None

    if nome != None and nome != '':
        if categoria != None and categoria != '':
                categoriaSelecionada = Categoria.objects.get(descricao=categoria)
                if (estado != '' and estado != None) and (cidade == '' or cidade == None):
                    produtos = Product.objects.filter(Q(alugado=False) & Q(nome__contains=nome) & Q(estado=estado)
                                                      & Q(categoria=categoriaSelecionada))
                elif cidade != '' and cidade != None:
                    produtos = Product.objects.filter(Q(alugado=False) & Q(nome__contains=nome) & Q(estado=estado)
                                                      & Q(cidade=cidade) & Q(categoria=categoriaSelecionada))
                else:
                    produtos = Product.objects.filter(Q(alugado=False) & Q(nome__contains=nome)
                                                      & Q(categoria=categoriaSelecionada))
        else:
            if (estado != '' and estado != None) and (cidade == '' or cidade == None):
                produtos = Product.objects.filter(Q(alugado=False) & Q(nome__contains=nome) & Q(estado=estado))
            elif cidade != '' and cidade != None:
                produtos = Product.objects.filter(
                    Q(alugado=False) & Q(nome__contains=nome) & Q(estado=estado) & Q(cidade=cidade))
            else:
                produtos = Product.objects.filter(Q(alugado=False) & Q(nome__contains=nome))

    elif nomeGET != None and nomeGET != '':
        nome = nomeGET
        if categoria != None and categoria != '':
            categoriaSelecionada = Categoria.objects.get(descricao=categoria)
            if (estado != '' and estado != None) and (cidade == '' or cidade == None):
                produtos = Product.objects.filter(
                    Q(alugado=False) & Q(nome__contains=nome) & Q(estado=estado) & Q(categoria=categoriaSelecionada))
            elif cidade != '' and cidade != None:
                produtos = Product.objects.filter(
                    Q(alugado=False) & Q(nome__contains=nome) & Q(estado=estado) & Q(cidade=cidade) & Q(
                        categoria=categoriaSelecionada))
            else:
                produtos = Product.objects.filter(Q(alugado=False) & Q(nome__contains=nome) & Q(categoria=categoriaSelecionada))
        else:
            if (estado != '' and estado != None) and (cidade == '' or cidade == None):
                produtos = Product.objects.filter(Q(alugado=False) & Q(nome__contains=nome) & Q(estado=estado))
            elif cidade != '' and cidade != None:
                produtos = Product.objects.filter(
                    Q(alugado=False) & Q(nome__contains=nome) & Q(estado=estado) & Q(cidade=cidade))
            else:
                produtos = Product.objects.filter(Q(alugado=False) & Q(nome__contains=nome))
    else:
        if categoria != None and categoria != '':
            categoriaSelecionada = Categoria.objects.get(descricao=categoria)
            if (estado != '' and estado != None) and (cidade == '' or cidade == None):
                produtos = Product.objects.filter(
                    Q(alugado=False) & Q(estado=estado) & Q(categoria=categoriaSelecionada))
            elif cidade != '' and cidade != None:
                produtos = Product.objects.filter(
                    Q(alugado=False) & Q(estado=estado) & Q(cidade=cidade) & Q(
                        categoria=categoriaSelecionada))
            else:
                produtos = Product.objects.filter(Q(alugado=False) & Q(categoria=categoriaSelecionada))
        else:
            if (estado != '' and estado != None) and (cidade == '' or cidade == None):
                produtos = Product.objects.filter(Q(alugado=False) & Q(nome__contains=nome) & Q(estado=estado))
            elif cidade != '' and cidade != None:
                produtos = Product.objects.filter(
                    Q(alugado=False) & Q(nome__contains=nome) & Q(estado=estado) & Q(cidade=cidade))
            else:
                produtos = Product.objects.filter(Q(alugado=False))

    paginator = Paginator(produtos, 10)

    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    if nome == None:
        nome = ''

    context = {
        'products': response,
        'nome': nome,
        'estado': estado,
        'cidade': cidade,
        'categoria': categoria
    }

    return render(request, 'pesquisa/pesquisa.html', context)

def gerarCategorias():
    categorias = Categoria.objects.all()
    descricoes = ["Agro e Indústria", "Automóveis", "Construção", "Eletrônicos", "Ferramentas", "Moda e Beleza", "Outros"]
    if len(categorias) == 0:
       for descricao in descricoes:
           categoria = Categoria()
           categoria.descricao = descricao
           categoria.save()

    elif len(categorias) == 6:
        categoria = Categoria()
        categoria.descricao = "Outros"
        categoria.save()
