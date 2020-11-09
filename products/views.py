from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


from . import filters
from .models import Product, Alugar
from users.models import MyUser
from address.models import Dados_usuario
from .forms import ProductForm, DenunciaForm, AlugarForm
from .filters import FilterCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def list_products(request, userId):
    user = MyUser.objects.get(id=userId)
    products = user.product_set.all()

    #aqui o usuario logado
    #print(request.user.id)

    #print('usuario logado acima, e abaixo, o id do usuario pelo parametro')

    #aqui, o usuario da url
    usu = MyUser.objects.get(id=userId)
    #print(usu.id)


    paginator = Paginator(products, 2)

    page = request.GET.get('page', 1)

    try:
        pagina = paginator.page(page)        
    except PageNotAnInteger:
        pagina = paginator.page(1) 
    except EmptyPage:
        pagina = paginator.page(paginator.num_pages)
    

    filtro = FilterCategory(request.GET, queryset=products)
    products = filtro.qs
    
    context = {'products': pagina, 'filtro': filtro, 'page':page}
    
    if request.user.id != usu.id:
        #print('diferentes')
        return render(request, 'home/home.html')
    else:
        #print('iguais')
        return render(request, 'products/my-products.html', context )

@login_required
def lista_products(request):    
    filtered_qs = filters.FilterCategory(
            request.GET,
            queryset=Product.objects.all()
        ).qs
    paginator = Paginator(filtered_qs, 4)

    page = request.GET.get('page')

    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    
    filtro = FilterCategory(request.GET, queryset=filtered_qs)
    context = {'products': response, 'filtro': filtro}

    return render(request, 'products/products.html', context)

@login_required
def create_product(request, userId):
    form = ProductForm(request.POST or None, request.FILES or None)
    user = MyUser.objects.get(id=userId)

    if form.is_valid():
        product = form.save(commit=False)
        product.user = user
        product.save()
        return redirect(reverse('list_products', kwargs={'userId': userId}))

    return render(request, 'products/products-form.html', {'form': form})

@login_required
def update_product(request, productId):
    product = get_object_or_404(Product, pk=productId)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        messages.info(request, 'Produto alterado com sucesso!')
        return render(request, 'products/my-products-detail.html', {'product': product})

    return render(request, 'products/products-alter-form.html', {'form': form, 'product': product})

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

#até aqui
    return render(request, 'products/products-detail.html', {'is_favourite': is_favourite, 'product': product})

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

#se der merda, apaga só aqui
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

        messages.info(request, 'O locador recebeu seu pedido de aluguel, aguarde o retorno dele, ou entre em contato com ele(a) pelo chat')
        return render(request, 'home/home.html')

    context = {
        'user': user,
        'produto': produto,
        'form': form,
        'locador':locador,
       # 'productId':productId

    }

    return render(request, 'products/alugarProduto.html', context)

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

def produtosRequisitados(request):
    user = request.user
    alugados = Alugar.objects.filter(Q(locador=user.id))
    return render(request, 'products/produtosRequisitados.html', {'alugados': alugados})

def detalharAluguel(request, idAluguel):
    user = request.user
    perfil = Dados_usuario.objects.get(user=user)
    aluguel = Alugar.objects.get(id=idAluguel)

    if perfil.nome == None or perfil.sobrenome == None:
        perfil.nome = user.email
    else:
        perfil.nome = perfil.nome + " " + perfil.sobrenome

    return render(request, 'products/detalharAluguel.html', {'perfil': perfil, 'aluguel': aluguel})
