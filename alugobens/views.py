from django.http import HttpResponse

from django.shortcuts import render, redirect, HttpResponseRedirect

from products.models import Product 

from products.forms import ProductForm

def hello(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def perfil(request):
    return render(request, 'perfil.html')

def home(request):
    return render(request, 'home.html')

def cadastro(request):
    return render(request, 'cadastro.html')

    #if request.method == 'POST':
     #   if Usuario.objects.filter(usuario_email=request.POST['usuario_email'], usuario_senha=request.POST['usuario_senha']).exists():
      #      usuarios = Usuario.objects.get(usuario_email=request.POST['usuario_email'], usuario_senha=request.POST['usuario_senha'])
       #     return render(request, 'home.html', {'usuarios': usuarios})
       # else:
       #     context = {'msg': 'Invalid email or password'}
       #     return render(request, 'login.html', context)

def list_products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('list_products')
        #products = Product.objects.all()
    	#return render(request, 'products.html')

    return render(request, 'products-form.html', {'form': form})

def update_product(request, id):
    product = Product.objects.get(id=id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('list_products')

    return render(request, 'products-form.html', {'form': form, 'product': product})

def delete_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('list_products')

    return render(request, 'prod-delete-confirm.html', {'product': product})
