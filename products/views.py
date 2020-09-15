from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product
from users.models import MyUser
from .forms import ProductForm


@login_required
def list_products(request, userId):
    user = MyUser.objects.get(id=userId)
    products = user.product_set.all()
    return render(request, 'products/products.html', {'products': products})

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
    userId = product.user.id

    if form.is_valid():
        form.save()
        return redirect(reverse('list_products', kwargs={'userId': userId}))

    return render(request, 'products/products-form.html', {'form': form, 'product': product})

@login_required
def delete_product(request, productId):
    product = Product.objects.get(id=productId)
    user = product.user
    product.delete()
    return redirect(reverse('list_products', kwargs={'userId': user.id}))

