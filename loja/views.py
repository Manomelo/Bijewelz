from django.shortcuts import render, get_object_or_404, redirect
from produtos.models import Produto, Categoria
from vendas.models import Carrinho, ItemCarrinho, Venda, ItemVenda
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
# Create your views here.

def inicio(request):
    produtos_destaque = Produto.objects.filter(qtd_estoque__gt=0, ativo=True)[:8]
    categorias = Categoria.objects.all()
    return render(request, 'loja/inicio.html', {
        'produtos_destaque': produtos_destaque,
        'categorias': categorias,
    })

def listar_produtos(request):
    produtos = Produto.objects.filter(qtd_estoque__gt=0, ativo=True)
    categorias = Categoria.objects.all()

    q = request.GET.get('q')
    preco_max = request.GET.get('preco_max')
    ordem = request.GET.get('ordem')
    categoria_slug = request.GET.get('categoria')

    if q:
        produtos = produtos.filter(nome__icontains=q)
    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)
    if categoria_slug:
        produtos = produtos.filter(categoria__slug=categoria_slug)
    if ordem == 'preco_asc':
        produtos = produtos.order_by('preco')
    elif ordem == 'preco_desc':
        produtos = produtos.order_by('-preco')
    elif ordem == 'nome':
        produtos = produtos.order_by('nome')

    return render(request, 'loja/produtos.html', {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_selecionada': categoria_slug,
    })

def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'loja/detalhe_produto.html', {'produto': produto})

@login_required
def ver_carrinho(request):
    carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
    return render(request, 'loja/carrinho.html', {'carrinho': carrinho})

@login_required
def adicionar_ao_carrinho(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    quantidade = int(request.POST.get('quantidade', 1))
    carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)


    item, criado = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
    if not criado:
        item.quantidade += quantidade
    else:
        item.quantidade = quantidade

    item.save()

    return redirect('loja_carrinho')

@login_required
def remover_do_carrinho(request, pk):
    carrinho = get_object_or_404(Carrinho, usuario = request.user)
    item = get_object_or_404(ItemCarrinho, carrinho=carrinho, produto__pk = pk)
    item.delete()
    return redirect('loja_carrinho')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('loja_inicio')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', 'loja_inicio'))
    else:
        form = AuthenticationForm()

    return render(request, 'loja/login.html', {'form': form})

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('loja_inicio')

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('loja_inicio')

    return render(request, 'loja/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('loja_inicio')

@login_required
def finalizar_pedido(request):
    carrinho = get_object_or_404(Carrinho, usuario=request.user)
    itens = carrinho.itens.select_related('produto').all()

    if not itens.exists():
        return redirect('loja_carrinho')

    erros = []
    for item in itens:
        if not item.produto.tem_estoque(item.quantidade):
            erros.append(f'{item.produto.nome} não tem estoque suficiente (disponível: {item.produto.qtd_estoque}).')

    if request.method == 'POST' and not erros:
        with transaction.atomic():
            venda = Venda.objects.create(
                total=carrinho.total(),
                usuario=request.user,
            )
            for item in itens:
                ItemVenda.objects.create(
                    venda=venda,
                    produto=item.produto,
                    quantidade=item.quantidade,
                    preco_unitario=item.produto.preco,
                )
                item.produto.qtd_estoque -= item.quantidade
                item.produto.save()
            carrinho.itens.all().delete()

        return redirect('loja_pedido_confirmado', pk=venda.pk)

    return render(request, 'loja/finalizar.html', {
        'carrinho': carrinho,
        'itens': itens,
        'erros': erros,
    })


@login_required
def pedido_confirmado(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    return render(request, 'loja/pedido_confirmado.html', {'venda': venda})

