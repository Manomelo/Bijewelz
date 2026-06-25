from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from produtos.models import Produto, Categoria
from vendas.models import Carrinho, ItemCarrinho, Venda


class LojaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(nome='Anéis', slug='aneis')
        self.produto = Produto.objects.create(
            nome='Anel de Prata',
            preco=49.90,
            qtd_estoque=10,
            estoque_minimo=2,
            categoria=self.categoria,
            ativo=True,
        )

    def test_pagina_inicial(self):
        response = self.client.get(reverse('loja_inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bijewelz')

    def test_listagem_produtos(self):
        response = self.client.get(reverse('loja_produtos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Anel de Prata')

    def test_listagem_filtro_busca(self):
        response = self.client.get(reverse('loja_produtos'), {'q': 'Anel'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Anel de Prata')

    def test_listagem_filtro_busca_sem_resultado(self):
        response = self.client.get(reverse('loja_produtos'), {'q': 'Produto Inexistente'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhum produto encontrado')

    def test_listagem_filtro_categoria(self):
        response = self.client.get(reverse('loja_produtos'), {'categoria': 'aneis'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Anel de Prata')

    def test_detalhe_produto(self):
        response = self.client.get(reverse('loja_detalhe_produto', args=[self.produto.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Anel de Prata')

    def test_detalhe_produto_inexistente(self):
        response = self.client.get(reverse('loja_detalhe_produto', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_produto_inativo_nao_aparece(self):
        self.produto.ativo = False
        self.produto.save()
        response = self.client.get(reverse('loja_produtos'))
        self.assertNotContains(response, 'Anel de Prata')


class CarrinhoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='lucas', password='senha123')
        self.produto = Produto.objects.create(
            nome='Pulseira',
            preco=29.90,
            qtd_estoque=5,
            estoque_minimo=1,
            ativo=True,
        )

    def test_carrinho_requer_login(self):
        response = self.client.get(reverse('loja_carrinho'))
        self.assertRedirects(response, '/loja/conta/login/?next=/loja/carrinho/')

    def test_adicionar_ao_carrinho(self):
        self.client.login(username='lucas', password='senha123')
        response = self.client.post(
            reverse('loja_adicionar_carrinho', args=[self.produto.pk]),
            {'quantidade': 2}
        )
        self.assertRedirects(response, reverse('loja_carrinho'))
        carrinho = Carrinho.objects.get(usuario=self.user)
        self.assertEqual(carrinho.itens.count(), 1)
        self.assertEqual(carrinho.itens.first().quantidade, 2)

    def test_adicionar_mesmo_produto_incrementa_quantidade(self):
        self.client.login(username='lucas', password='senha123')
        self.client.post(reverse('loja_adicionar_carrinho', args=[self.produto.pk]), {'quantidade': 1})
        self.client.post(reverse('loja_adicionar_carrinho', args=[self.produto.pk]), {'quantidade': 2})
        carrinho = Carrinho.objects.get(usuario=self.user)
        self.assertEqual(carrinho.itens.first().quantidade, 3)

    def test_remover_do_carrinho(self):
        self.client.login(username='lucas', password='senha123')
        self.client.post(reverse('loja_adicionar_carrinho', args=[self.produto.pk]), {'quantidade': 1})
        response = self.client.post(reverse('loja_remover_carrinho', args=[self.produto.pk]))
        self.assertRedirects(response, reverse('loja_carrinho'))
        carrinho = Carrinho.objects.get(usuario=self.user)
        self.assertEqual(carrinho.itens.count(), 0)

    def test_ver_carrinho(self):
        self.client.login(username='lucas', password='senha123')
        self.client.post(reverse('loja_adicionar_carrinho', args=[self.produto.pk]), {'quantidade': 1})
        response = self.client.get(reverse('loja_carrinho'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pulseira')


class LoginRegistroTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='lucas', password='senha123')

    def test_pagina_login(self):
        response = self.client.get(reverse('loja_login'))
        self.assertEqual(response.status_code, 200)

    def test_login_valido(self):
        response = self.client.post(reverse('loja_login'), {
            'username': 'lucas',
            'password': 'senha123',
        })
        self.assertRedirects(response, reverse('loja_inicio'))

    def test_login_invalido(self):
        response = self.client.post(reverse('loja_login'), {
            'username': 'lucas',
            'password': 'senhaerrada',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'inválidos')

    def test_login_redireciona_se_autenticado(self):
        self.client.login(username='lucas', password='senha123')
        response = self.client.get(reverse('loja_login'))
        self.assertRedirects(response, reverse('loja_inicio'))

    def test_pagina_registro(self):
        response = self.client.get(reverse('loja_registro'))
        self.assertEqual(response.status_code, 200)

    def test_registro_valido(self):
        response = self.client.post(reverse('loja_registro'), {
            'username': 'novo_user',
            'password1': 'senhaForte123',
            'password2': 'senhaForte123',
        })
        self.assertRedirects(response, reverse('loja_inicio'))
        self.assertTrue(User.objects.filter(username='novo_user').exists())

    def test_logout(self):
        self.client.login(username='lucas', password='senha123')
        response = self.client.get(reverse('loja_logout'))
        self.assertRedirects(response, reverse('loja_inicio'))


class FinalizarPedidoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='lucas', password='senha123')
        self.produto = Produto.objects.create(
            nome='Colar',
            preco=99.90,
            qtd_estoque=5,
            estoque_minimo=1,
            ativo=True,
        )

    def test_finalizar_requer_login(self):
        response = self.client.get(reverse('loja_finalizar'))
        self.assertRedirects(response, '/loja/conta/login/?next=/loja/finalizar/')

    def test_finalizar_pedido(self):
        self.client.login(username='lucas', password='senha123')
        self.client.post(reverse('loja_adicionar_carrinho', args=[self.produto.pk]), {'quantidade': 2})
        response = self.client.post(reverse('loja_finalizar'))
        self.assertEqual(Venda.objects.count(), 1)
        venda = Venda.objects.first()
        self.assertEqual(venda.usuario, self.user)
        self.assertRedirects(response, reverse('loja_pedido_confirmado', args=[venda.pk]))

    def test_finalizar_reduz_estoque(self):
        self.client.login(username='lucas', password='senha123')
        self.client.post(reverse('loja_adicionar_carrinho', args=[self.produto.pk]), {'quantidade': 3})
        self.client.post(reverse('loja_finalizar'))
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.qtd_estoque, 2)

    def test_finalizar_esvazia_carrinho(self):
        self.client.login(username='lucas', password='senha123')
        self.client.post(reverse('loja_adicionar_carrinho', args=[self.produto.pk]), {'quantidade': 1})
        self.client.post(reverse('loja_finalizar'))
        carrinho = Carrinho.objects.get(usuario=self.user)
        self.assertEqual(carrinho.itens.count(), 0)

    def test_finalizar_estoque_insuficiente(self):
        self.client.login(username='lucas', password='senha123')
        self.client.post(reverse('loja_adicionar_carrinho', args=[self.produto.pk]), {'quantidade': 1})
        self.produto.qtd_estoque = 0
        self.produto.save()
        response = self.client.post(reverse('loja_finalizar'))
        self.assertEqual(Venda.objects.count(), 0)
        self.assertContains(response, 'estoque')