from django.test import TestCase, Client
from django.urls import reverse
from .models import Produto


class ProdutoModelTest(TestCase):
    def setUp(self):
        self.produto = Produto.objects.create(
            nome='Anel de Prata',
            preco=49.90,
            qtd_estoque=10,
            estoque_minimo=3,
        )

    def test_str(self):
        self.assertEqual(str(self.produto), 'Anel de Prata')

    def test_tem_estoque_suficiente(self):
        self.assertTrue(self.produto.tem_estoque(5))

    def test_tem_estoque_insuficiente(self):
        self.assertFalse(self.produto.tem_estoque(15))

    def test_estoque_nao_baixo(self):
        self.assertFalse(self.produto.estoque_baixo())

    def test_estoque_baixo(self):
        self.produto.qtd_estoque = 2
        self.produto.save()
        self.assertTrue(self.produto.estoque_baixo())


class ProdutoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.produto = Produto.objects.create(
            nome='Colar Dourado',
            preco=89.90,
            qtd_estoque=5,
            estoque_minimo=1,
        )

    def test_listar(self):
        response = self.client.get(reverse('listar_produtos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Colar Dourado')

    def test_criar(self):
        response = self.client.post(reverse('criar_produto'), {
            'nome': 'Brinco de Ouro',
            'descricao': '',
            'preco': '39.90',
            'qtd_estoque': 20,
            'estoque_minimo': 5,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Produto.objects.count(), 2)

    def test_editar(self):
        response = self.client.post(
            reverse('editar_produto', args=[self.produto.pk]),
            {'nome': 'Colar Editado', 'descricao': '', 'preco': '99.90', 'qtd_estoque': 5, 'estoque_minimo': 1},
        )
        self.assertEqual(response.status_code, 302)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'Colar Editado')

    def test_excluir(self):
        response = self.client.post(reverse('excluir_produto', args=[self.produto.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Produto.objects.count(), 0)
