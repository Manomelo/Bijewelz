from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import ProtectedError
from .models import Produto, Categoria
from .forms import ProdutoForm, CategoriaForm


def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/listar.html', {'produtos': produtos})


def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form.html', {'form': form, 'titulo': 'Novo Produto'})


def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/form.html', {'form': form, 'titulo': 'Editar Produto'})


def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        try:
            produto.delete()
        except ProtectedError:
            produto.ativo = False
            produto.save()
        return redirect('listar_produtos')
    return render(request, 'produtos/confirmar_exclusao.html', {'produto': produto})


def ativar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    produto.ativo = True
    produto.save()
    return redirect('listar_produtos')


def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'produtos/categorias/listar.html', {'categorias': categorias})


def criar_categoria(request):
    form = CategoriaForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('listar_categorias')
    return render(request, 'produtos/categorias/form.html', {'form': form, 'titulo': 'Nova Categoria'})


def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, request.FILES or None, instance=categoria)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('listar_categorias')
    return render(request, 'produtos/categorias/form.html', {'form': form, 'titulo': 'Editar Categoria'})


def excluir_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'produtos/categorias/confirmar_exclusao.html', {'categoria': categoria})