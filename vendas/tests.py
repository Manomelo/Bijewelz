from django.test import TestCase, Client
from django.urls import reverse
from clientes.models import Cliente
from produtos.models import Produto
from .models import Venda, ItemVenda


class VendaModelTest(TestCase):
    def setUp(self):
        self.produto = Produto.objects.create(
            nome='Pulseira', preco=29.90, qtd_estoque=10, estoque_minimo=2
        )
        self.cliente = Cliente.objects.create(
            nome='Carlos', cpf='111.111.111-11', email='carlos@email.com'
        )
        self.venda = Venda.objects.create(cliente=self.cliente, total=29.90)
        ItemVenda.objects.create(
            venda=self.venda, produto=self.produto, quantidade=1, preco_unitario=29.90
        )

    def test_str(self):
        self.assertEqual(str(self.venda), f'Venda #{self.venda.pk}')

    def test_subtotal_item(self):
        item = self.venda.itens.first()
        from decimal import Decimal
        self.assertEqual(item.subtotal, Decimal('29.90'))


class NovaVendaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.produto = Produto.objects.create(
            nome='Anel', preco=50.00, qtd_estoque=5, estoque_minimo=1
        )

    def test_registrar_venda_reduz_estoque(self):
        response = self.client.post(reverse('nova_venda'), {
            'cliente': '',
            'produto': [str(self.produto.pk)],
            'quantidade': ['2'],
        })
        self.assertEqual(response.status_code, 302)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.qtd_estoque, 3)
        self.assertEqual(Venda.objects.count(), 1)

    def test_estoque_insuficiente_retorna_erro(self):
        response = self.client.post(reverse('nova_venda'), {
            'cliente': '',
            'produto': [str(self.produto.pk)],
            'quantidade': ['99'],
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Estoque insuficiente')
        self.assertEqual(Venda.objects.count(), 0)

    def test_venda_sem_itens_retorna_erro(self):
        response = self.client.post(reverse('nova_venda'), {
            'cliente': '',
            'produto': [''],
            'quantidade': [''],
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'pelo menos um item')


class RelatorioVendasTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.venda = Venda.objects.create(total=100.00)

    def test_relatorio_sem_filtro(self):
        response = self.client.get(reverse('relatorio_vendas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '100')
