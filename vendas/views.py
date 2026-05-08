from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Venda, ItemVenda
from clientes.models import Cliente
from produtos.models import Produto


def listar_vendas(request):
    vendas = Venda.objects.all()
    return render(request, 'vendas/listar.html', {'vendas': vendas})


def nova_venda(request):
    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente') or None
        produto_ids = request.POST.getlist('produto')
        quantidades = request.POST.getlist('quantidade')

        erros = []
        itens_validos = []

        for pid, qtd_str in zip(produto_ids, quantidades):
            if not pid or not qtd_str:
                continue
            try:
                produto = Produto.objects.get(pk=pid)
                qtd = int(qtd_str)
                if qtd <= 0:
                    erros.append(f'Quantidade inválida para {produto.nome}.')
                elif not produto.tem_estoque(qtd):
                    erros.append(f'Estoque insuficiente para {produto.nome} (disponível: {produto.qtd_estoque}).')
                else:
                    itens_validos.append((produto, qtd))
            except (Produto.DoesNotExist, ValueError):
                erros.append('Produto ou quantidade inválidos.')

        if not itens_validos:
            erros.append('Adicione pelo menos um item à venda.')

        if erros:
            return render(request, 'vendas/nova.html', {
                'clientes': clientes,
                'produtos': produtos,
                'erros': erros,
            })

        with transaction.atomic():
            cliente = Cliente.objects.filter(pk=cliente_id).first() if cliente_id else None
            total = sum(p.preco * q for p, q in itens_validos)
            venda = Venda.objects.create(cliente=cliente, total=total)
            for produto, qtd in itens_validos:
                ItemVenda.objects.create(
                    venda=venda,
                    produto=produto,
                    quantidade=qtd,
                    preco_unitario=produto.preco,
                )
                produto.qtd_estoque -= qtd
                produto.save()

        return redirect('detalhe_venda', pk=venda.pk)

    return render(request, 'vendas/nova.html', {'clientes': clientes, 'produtos': produtos})


def detalhe_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    return render(request, 'vendas/detalhe.html', {'venda': venda})


def relatorio_vendas(request):
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    vendas = Venda.objects.all()
    if data_inicio:
        vendas = vendas.filter(data_venda__date__gte=data_inicio)
    if data_fim:
        vendas = vendas.filter(data_venda__date__lte=data_fim)

    total_receita = sum(v.total for v in vendas)

    return render(request, 'relatorios/vendas.html', {
        'vendas': vendas,
        'total_receita': total_receita,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    })
