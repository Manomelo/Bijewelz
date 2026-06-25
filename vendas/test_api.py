from rest_framework.test import APITestCase
from clientes.models import Cliente
from produtos.models import Produto
from .models import Venda, ItemVenda


class VendaAPITest(APITestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome='Carlos',
            cpf='111.111.111-11',
            email='carlos@email.com',
        )
        self.produto = Produto.objects.create(
            nome='Pulseira',
            preco=29.90,
            qtd_estoque=10,
            estoque_minimo=2,
        )
        self.venda = Venda.objects.create(
            cliente=self.cliente,
            total=29.90,
        )
        ItemVenda.objects.create(
            venda=self.venda,
            produto=self.produto,
            quantidade=1,
            preco_unitario=29.90,
        )

    def test_listar_vendas(self):
        response = self.client.get('/api/vendas/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_detalhe_venda(self):
        response = self.client.get(f'/api/vendas/{self.venda.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], '29.90')

    def test_detalhe_venda_contem_itens(self):
        response = self.client.get(f'/api/vendas/{self.venda.pk}/')
        self.assertIn('itens', response.data)
        self.assertEqual(len(response.data['itens']), 1)

    def test_detalhe_venda_item_contem_subtotal(self):
        response = self.client.get(f'/api/vendas/{self.venda.pk}/')
        item = response.data['itens'][0]
        self.assertIn('subtotal', item)
        self.assertEqual(item['subtotal'], '29.90')

    def test_detalhe_venda_item_contem_produto_detalhe(self):
        response = self.client.get(f'/api/vendas/{self.venda.pk}/')
        item = response.data['itens'][0]
        self.assertIn('produto_detalhe', item)
        self.assertEqual(item['produto_detalhe']['nome'], 'Pulseira')

    def test_detalhe_venda_inexistente(self):
        response = self.client.get('/api/vendas/9999/')
        self.assertEqual(response.status_code, 404)

    def test_venda_sem_cliente(self):
        venda = Venda.objects.create(total=50.00)
        response = self.client.get(f'/api/vendas/{venda.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data['cliente'])