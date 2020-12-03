from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.shortcuts import reverse, get_object_or_404

from address.models import Dados_usuario
from ratings.models import HistoricoAlugados
from users.models import MyUser
from .filters import FilterCategory
from .forms import ProductForm, DenunciaForm, AlugarForm
from .models import Product, Alugar, HistoricoStatus, StatusAguardando, StatusCancelado, StatusAceito, StatusEncerrado


@login_required
def list_products(request, userId):
    user = MyUser.objects.get(id=userId)
    products = Product.objects.filter(Q(user=user, alugado=False))
    quantidade = len(products)

    usu = MyUser.objects.get(id=userId)

    paginator = Paginator(products, 6)

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
        return render(request, 'home/home.html')
    else:
        return render(request, 'products/my-products.html', context)


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

    return render(request, 'products/products-alter-form.html',
                  {'form': form, 'product': product, 'estado': product.estado, 'cidade': product.cidade})


@login_required
def delete_product(request, productId):
    product = Product.objects.get(id=productId)
    user = product.user
    product.delete()
    messages.info(request, 'Produto excluido com sucesso!')
    return redirect(reverse('list_products', kwargs={'userId': user.id}))


def detail_product(request, id):
    product = get_object_or_404(Product, pk=id)

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
                  {'is_favourite': is_favourite, 'product': product, 'identificador': identificador})


@login_required
def favourite_products(request, id):
    product = get_object_or_404(Product, id=id)
    url = request.META.get('HTTP_REFERER')

    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
        return HttpResponseRedirect(url)
    else:
        product.favourite.add(request.user)
        return HttpResponseRedirect(url)

    return render(request, 'products/products-detail.html', {'product': product})


@login_required
def products_favourite_list(request):
    user = request.user
    favourite_products = user.favourite.all()
    quantidade = len(favourite_products)

    context = {'favourite_products': favourite_products, 'quantidade': quantidade,

    }
    return render(request, 'products/products_favourite_list.html', context)


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

    return render(request, 'products/alugar.html',
                  {'cpf': perfil.cpf if perfil.cpf != None else "", 'cep': perfil.cep if perfil.cep != None else "",
                      'cidade': perfil.cidade if perfil.cidade != None else "",
                      'estado': perfil.estado if perfil.estado != None else "",
                      'rua': perfil.rua if perfil.rua != None else "",
                      'bairro': perfil.bairro if perfil.bairro != None else "",
                      'complemento': perfil.complemento if perfil.complemento != None else "", })


@login_required
def alugarSubmit(request, productId):
    user = request.user
    form = AlugarForm(request.POST or None)
    produto = Product.objects.get(id=productId)
    if request.POST.get("id_cpf") != None:
        salvarPerfil(request)
    locador1 = produto.user.id
    locador = MyUser.objects.get(id=locador1)

    if request.POST and form.is_valid():
        alugar = form.save(commit=False)
        alugar.locatario = user
        alugar.locador = locador
        alugar.produto = produto
        alugar.inicio = str(form.cleaned_data['inicio'])
        alugar.fim = str(form.cleaned_data['fim'])
        alugar.confirmado = False
        alugar.save()

        status = StatusAguardando()
        status.locador = locador
        status.locatario = user
        status.produto = produto
        status.encerrado = False
        status.save()

        messages.info(request,
                      'O locador recebeu seu pedido de aluguel, aguarde o retorno dele, ou entre em contato com ele(a) pelo chat')
        is_favourite = False
        if produto.favourite.filter(id=request.user.id).exists():
            is_favourite = True
        try:
            perfil = Dados_usuario.objects.get(user=produto.user)
        except ObjectDoesNotExist:
            perfil = Dados_usuario()

        if perfil.nome != None:
            identificador = perfil.nome
        else:
            identificador = 'Anônimo'
        return render(request, 'products/products-detail.html', {'is_favourite': is_favourite, 'product': produto, 'identificador': identificador})

    context = {'user': user, 'produto': produto, 'form': form, 'locador': locador, # 'productId':productId

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
    perfil.user = user
    perfil.save()


@login_required
def produtosRequisitados(request):
    user = request.user
    alugados = Alugar.objects.filter(Q(locador=user) & Q(confirmado=True))
    propostas = Alugar.objects.filter(Q(locador=user) & Q(confirmado=False))
    return render(request, 'products/produtosRequisitados.html', {'alugados': alugados, 'propostas': propostas})


@login_required
def detalharAluguel(request, idAluguel):
    user = request.user
    aluguel = Alugar.objects.get(id=idAluguel)
    perfilLocatario = Dados_usuario.objects.get(user=aluguel.locatario)

    if perfilLocatario.nome == None or perfilLocatario.sobrenome == None:
        identificador = aluguel.locatario.email
    else:
        identificador = perfilLocatario.nome + " " + perfilLocatario.sobrenome

    return render(request, 'products/detalharAluguel.html',
                  {'perfilLocatario': perfilLocatario, 'aluguel': aluguel, 'identificador': identificador})


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

    locador = aluguel.locador
    locatario = aluguel.locatario
    produto = aluguel.produto

    historicoAlugados = HistoricoAlugados()

    historicoAlugados.locador = locador
    historicoAlugados.locatario = locatario
    historicoAlugados.produto = produto
    historicoAlugados.encerrado = True
    historicoAlugados.save()

    status = StatusEncerrado()
    status.locador = locador
    status.locatario = locatario
    status.produto = produto
    status.encerrado = True
    status.save()

    a = pro
    produto = Product.objects.get(id=pro)
    produto.alugado = False
    produto.save()

    aluguel.delete()

    messages.info(request, 'Você encerrou um aluguel, por gentileza avalie a experiência com o locatario')
    return render(request, 'products/produtosRequisitados.html')


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

    aluguel.delete()

    messages.info(request, 'Você cancelou a proposta de aluguel')
    return render(request, 'products/produtosRequisitados.html')


@login_required
def historicoStatus(request):
    user = request.user
    historico = reversed(HistoricoStatus.objects.filter(Q(locatario=user)))
    return render(request, 'user/historicoStatus.html', {'historicos': historico})
