from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


from . import filters
from .models import Product, Alugar, Categoria, HistoricoStatus, StatusAguardando, StatusCancelado, StatusAceito, StatusEncerrado
from users.models import MyUser
from address.models import Dados_usuario
from .forms import ProductForm, DenunciaForm, AlugarForm
from .filters import FilterCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ratings.models import HistoricoAlugados, Rating

from django.shortcuts import render, redirect, HttpResponseRedirect,HttpResponse


@login_required
def list_products(request, userId):
    user = MyUser.objects.get(id=userId)
    products = Product.objects.filter(Q(user=user, alugado=False))
    quantidade = len(products)

    #aqui o usuario logado
    #print(request.user.id)

    #print('usuario logado acima, e abaixo, o id do usuario pelo parametro')

    #aqui, o usuario da url
    usu = MyUser.objects.get(id=userId)
    #print(usu.id)


    paginator = Paginator(products, 4)

    page = request.GET.get('page', 1)

    try:
        pagina = paginator.page(page)        
    except PageNotAnInteger:
        pagina = paginator.page(1) 
    except EmptyPage:
        pagina = paginator.page(paginator.num_pages)
    

    filtro = FilterCategory(request.GET, queryset=products)
    products = filtro.qs
    
    context = {'products': pagina, 'filtro': filtro, 'page': page, 'quantidade': quantidade}
    
    if request.user.id != usu.id:
        #print('diferentes')
        return render(request, 'home/home.html')
    else:
        #print('iguais')
        return render(request, 'products/my-products.html', context)

def lista_products(request):
    produtos = Product.objects.filter(Q(alugado=False)).order_by('-id')[0:8]

    context = {'products': produtos}

    return render(request, 'home/home.html', context)

@login_required
def create_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    user = request.user
    if form.is_valid():
        product = form.save(commit=False)
        product.user = user
        product.cidade = request.POST.get('cidade')
        product.estado = request.POST.get('estado')
        product.save()
        messages.info(request, 'Anunciado com sucesso!')
        form = ProductForm(None, None)
        return render(request, 'products/products-form.html', {'form': form})


    return render(request, 'products/products-form.html', {'form': form})

@login_required
def update_product(request, productId):
    product = get_object_or_404(Product, pk=productId)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        product.cidade = request.POST.get('cidade')
        product.estado = request.POST.get('estado')
        product.save()
        messages.info(request, 'Anúncio alterado com sucesso!')
        return render(request, 'products/products-alter-form.html',
                      {'form': form, 'product': product, 'estado': product.estado, 'cidade': product.cidade})

    return render(request, 'products/products-alter-form.html', {
        'form': form,
        'product': product,
        'estado': product.estado,
        'cidade': product.cidade
    })

@login_required
def delete_product(request, productId):
    product = Product.objects.get(id=productId)
    user = product.user
    product.delete()
    messages.info(request, 'Produto excluido com sucesso!')
    return redirect(reverse('list_products', kwargs={'userId': user.id}))

@login_required
def detail_product(request, id):
    product = get_object_or_404(Product, pk=id)
    
    #se der merda. apagar isso
    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
       is_favourite = True

    try:
        perfil = Dados_usuario.objects.get(user=product.user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    if perfil.nome != None:
        identificador = perfil.nome
    else:
        identificador = 'Anônimo'

    return render(request, 'products/products-detail.html',
                  {'is_favourite': is_favourite,
                   'product': product,
                   'identificador': identificador
                   })

@login_required
def my_detail_product(request, productId):
    product = get_object_or_404(Product, pk=productId)
    #usuario logado
    user = request.user
    usuarioLogado = user.id
    #aqui, o usuario da url
    usu = MyUser.objects.get(id=product.user.id)
    usuarioQueCadastrou = usu.id
    #print('id DO usuario logado')    
    #print(usuarioLogado)
    #print('id do usuario que cadastrou')
    #print(usu.id)    
    
    if usuarioLogado != usuarioQueCadastrou:
        return render(request, 'home/home.html')
    else:  
        return render(request, 'products/my-products-detail.html', {'product': product})

@login_required
def favourite_products(request, id):
    product = get_object_or_404(Product, id=id)
    #user = request.user
 
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
        #print('removeu')
    else:
        product.favourite.add(request.user)
        #print('adiciounou')
    #print('cima')
    
    #print('baixo')

    #return HttpResponseRedirect(product.get_absolute_url(), 'products/products-detail.html')
    return render(request, 'products/products-detail.html', {'product':product})


@login_required
def products_favourite_list(request):    
    user = request.user
    favourite_products = user.favourite.all()

    context = {
        'favourite_products': favourite_products,

    }
    #return render(request, 'products/products-detail.html', context)
    return render(request, 'products/products_favourite_list.html', context)
#    return render(request, 'products/products-detail.html', {'product': product})

@login_required
def denunciar(request, productId):
    form = DenunciaForm(request.POST or None)
    user = request.user
    produto = Product.objects.get(id=productId)

    if form.is_valid():
        denuncia = form.save(commit=False)
        denuncia.user = user
        denuncia.produto = produto
        denuncia.save()
        messages.info(request, 'Agradecemos pela sua boa '
                               'vontade de manter a nossa plataforma mais acolhedora '
                               'e iremos avaliar esse caso!')
        return redirect(reverse('denuncia', kwargs={'productId': produto.id}))

    return render(request, 'products/denuncia.html', {'form': form, 'productId': produto.id})

@login_required
def alugar(request, productId):
    user = request.user
  
    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    messages.info(request, 'Por gentileza, confirme seus dados!')
    return render(request, 'products/alugar.html', {
        'cpf': perfil.cpf if perfil.cpf != None else "",
        'cep': perfil.cep if perfil.cep != None else "",
        'cidade': perfil.cidade if perfil.cidade != None else "",
        'estado': perfil.estado if perfil.estado != None else "",
        'rua': perfil.rua if perfil.rua != None else "",
        'bairro': perfil.bairro if perfil.bairro != None else "",
        'complemento': perfil.complemento if perfil.complemento != None else "",
    })


@login_required
def alugarSubmit(request, productId):
    user = request.user
    form = AlugarForm(request.POST or None)
    produto = Product.objects.get(id=productId)
    if request.POST.get("id_cpf") != None:
        salvarPerfil(request)
    locador1 = produto.user.id
    locador = MyUser.objects.get(id=locador1)
    #print(locatario)
    print('ID DO locatariooo')
    print(produto.user.id)
    print('ID DO locatariooo')

    if request.POST and form.is_valid():
        alugar = form.save(commit=False)
        
        alugar.locatario = user
        alugar.locador = locador
        #alugar.locatario = 
        alugar.produto = produto
        alugar.inicio = str(form.cleaned_data['inicio']) 
        alugar.fim = str(form.cleaned_data['fim'])
        alugar.confirmado = False
        #alugar.inicio = str(begin[0])
        #alugar.fim = str(end[0])
        print('DATA')
        print(alugar.inicio[0])
        print(alugar.fim)
        alugar.save()

        status = StatusAguardando()
        status.locador = locador
        status.locatario = user        
        status.produto = produto
        status.encerrado = False
        status.save()

        messages.info(request, 'O locador recebeu seu pedido de aluguel, aguarde o retorno dele, ou entre em contato com ele(a) pelo chat')
        is_favourite = False
        if produto.favourite.filter(id=request.user.id).exists():
            is_favourite = True
        return render(request, 'products/products-detail.html', {'is_favourite': is_favourite, 'product': produto})

    context = {
        'user': user,
        'produto': produto,
        'form': form,
        'locador':locador,
       # 'productId':productId

    }

    return render(request, 'products/alugarProduto.html', context)

@login_required
def salvarPerfil(request):
    user = request.user

    try:
        perfil = Dados_usuario.objects.get(user=user)
    except ObjectDoesNotExist:
        perfil = Dados_usuario()

    perfil.cpf = request.POST.get("id_cpf")
    perfil.cep = request.POST.get("id_cep")
    perfil.rua = request.POST.get("id_rua")
    perfil.bairro = request.POST.get("id_bairro")
    perfil.cidade = request.POST.get("id_cidade")
    perfil.estado = request.POST.get("id_estado")
    perfil.complemento = request.POST.get("id_complemento")
    perfil.save()

@login_required
def produtosRequisitados(request):
    user = request.user
    alugados = Alugar.objects.filter(Q(locador=user))
    return render(request, 'products/produtosRequisitados.html', {'alugados': alugados})

@login_required
def detalharAluguel(request, idAluguel):
    user = request.user
    aluguel = Alugar.objects.get(id=idAluguel)
    perfilLocatario = Dados_usuario.objects.get(user=aluguel.locatario)

    if perfilLocatario.nome == None or perfilLocatario.sobrenome == None:
        identificador = aluguel.locatario.email
    else:
        identificador = perfilLocatario.nome + " " + perfilLocatario.sobrenome

    return render(request, 'products/detalharAluguel.html', {
        'perfilLocatario': perfilLocatario,
        'aluguel': aluguel,
        'identificador': identificador})


@login_required
def confirmarAluguel(request, idAluguel):
    user = request.user
    aluguel = Alugar.objects.get(id=idAluguel)
    perfilLocatario = Dados_usuario.objects.get(user=aluguel.locatario)

    if perfilLocatario.nome == None or perfilLocatario.sobrenome == None:
        identificador = aluguel.locatario.email
    else:
        identificador = perfilLocatario.nome + " " + perfilLocatario.sobrenome

    pro = aluguel.produto.id

    produto = Product.objects.get(id=pro)    
   

    aluguel.confirmado = True    
    aluguel.save()
    
    
    produto.alugado = True    
    produto.save()
    
    locador = aluguel.locador
    locatario = aluguel.locatario
    pro = aluguel.produto

    status = StatusAceito()
    status.locador = locador
    status.locatario = locatario        
    status.produto = produto
    status.encerrado = False
    status.save()

    return render(request, 'products/detalharAluguel.html',
                  {'perfilLocatario': perfilLocatario, 'aluguel': aluguel, 'identificador': identificador})

@login_required
def encerrarAluguel(request, idAluguel):
    user = request.user
    aluguel = Alugar.objects.get(id=idAluguel)
    
    pro = aluguel.produto.id

     #historicoAlugados
    locador = aluguel.locador
    locatario = aluguel.locatario
    produto = aluguel.produto

    historicoAlugados = HistoricoAlugados()

    historicoAlugados.locador = locador
    historicoAlugados.locatario = locatario
    historicoAlugados.produto = produto
    historicoAlugados.encerrado = True
    historicoAlugados.save()

    #HistoricoStatus
    status = StatusEncerrado()
    status.locador = locador
    status.locatario = locatario        
    status.produto = produto
    status.encerrado = True
    status.save()
    #historicoAlugados
    #avaliação
    #isso não faz sentido
    #avaliar = Rating()
    #avaliar.de = locador
    #avaliar.para = locatario
    #avaliar.save()
    #avaliação

    a = pro
    produto = Product.objects.get(id=pro)     
    produto.alugado = False    
    produto.save()

   
    #aluguel.confirmado = False    
    aluguel.delete()

    #context = {
    #'aluguel': aluguel,
    #}
    
    messages.info(request, 'Você encerrou um aluguel, por gentileza avalie a experiência com o locatario')
    return render(request, 'products/produtosRequisitados.html')
    #return redirect(reverse('produtos_requisitados', kwargs={'user': user}))



@login_required
def cancelarAluguel(request, idAluguel):
    user = request.user
    aluguel = Alugar.objects.get(id=idAluguel)
    
    pro = aluguel.produto.id

     
    locador = aluguel.locador
    locatario = aluguel.locatario
    produto = aluguel.produto
    
    status = StatusCancelado()
    status.locador = locador
    status.locatario = locatario        
    status.produto = produto
    status.encerrado = False
    status.save()

    print('ME DIZ ONDE ESTÁ ERRADO AQUI POHAAAAAA, MSSSSSSS')  
    aluguel.delete()

    #context = {
    #'aluguel': aluguel,
    #}
    
    messages.info(request, 'Você cancelou a proposta de aluguel')
    return render(request, 'products/produtosRequisitados.html')
   
@login_required
def historicoStatus(request):
    user = request.user
    historico = reversed(HistoricoStatus.objects.filter(Q(locatario=user)))
    return render(request, 'user/historicoStatus.html', {'historicos': historico})
