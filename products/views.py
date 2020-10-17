from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect 

from . import filters
from .models import Product, Categoria
from users.models import MyUser
from .forms import ProductForm
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
    paginator = Paginator(filtered_qs, 2)

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
