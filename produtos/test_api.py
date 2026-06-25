from rest_framework.test import APITestCase
from .models import Produto


class ProdutoAPITest(APITestCase):
    def setUp(self):
        self.produto = Produto.objects.create(
            nome='Anel de Prata',
            preco=49.90,
            qtd_estoque=10,
            estoque_minimo=3,
        )

    def test_listar_produtos(self):
        response = self.client.get('/api/produtos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_detalhe_produto(self):
        response = self.client.get(f'/api/produtos/{self.produto.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nome'], 'Anel de Prata')

    def test_detalhe_produto_campo_estoque_baixo(self):
        response = self.client.get(f'/api/produtos/{self.produto.pk}/')
        self.assertIn('estoque_baixo', response.data)
        self.assertFalse(response.data['estoque_baixo'])

    def test_detalhe_produto_estoque_baixo_verdadeiro(self):
        self.produto.qtd_estoque = 2
        self.produto.save()
        response = self.client.get(f'/api/produtos/{self.produto.pk}/')
        self.assertTrue(response.data['estoque_baixo'])

    def test_criar_produto(self):
        response = self.client.post('/api/produtos/', {
            'nome': 'Colar Dourado',
            'preco': '89.90',
            'qtd_estoque': 5,
            'estoque_minimo': 1,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Produto.objects.count(), 2)

    def test_editar_produto(self):
        response = self.client.put(f'/api/produtos/{self.produto.pk}/', {
            'nome': 'Anel Editado',
            'preco': '59.90',
            'qtd_estoque': 10,
            'estoque_minimo': 3,
        })
        self.assertEqual(response.status_code, 200)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'Anel Editado')

    def test_excluir_produto(self):
        response = self.client.delete(f'/api/produtos/{self.produto.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Produto.objects.count(), 0)

    def test_detalhe_produto_inexistente(self):
        response = self.client.get('/api/produtos/9999/')
        self.assertEqual(response.status_code, 404)