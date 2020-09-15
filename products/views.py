from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Product
from .forms import ProductForm


@login_required
def list_products(request):
    products = Product.objects.all()
    return render(request, 'products/products.html', {'products': products})

@login_required
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('list_products')

    return render(request, 'products/products-form.html', {'form': form})

@login_required
def update_product(request, id):
    product = Product.objects.get(id=id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('list_products')

    return render(request, 'products/products-form.html', {'form': form, 'product': product})

@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('list_products')

    return render(request, 'products/prod-delete-confirm.html', {'product': product})
