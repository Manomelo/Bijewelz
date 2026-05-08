from django.test import TestCase, Client
from django.urls import reverse
from .models import Cliente


class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome='Ana Silva',
            cpf='123.456.789-00',
            email='ana@email.com',
            telefone='11999999999',
        )

    def test_str(self):
        self.assertEqual(str(self.cliente), 'Ana Silva')

    def test_criacao(self):
        self.assertEqual(Cliente.objects.count(), 1)


class ClienteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cliente = Cliente.objects.create(
            nome='João Santos',
            cpf='987.654.321-00',
            email='joao@email.com',
        )

    def test_listar(self):
        response = self.client.get(reverse('listar_clientes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Santos')

    def test_criar(self):
        response = self.client.post(reverse('criar_cliente'), {
            'nome': 'Maria Oliveira',
            'cpf': '111.222.333-44',
            'email': 'maria@email.com',
            'telefone': '',
            'endereco': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_editar(self):
        response = self.client.post(
            reverse('editar_cliente', args=[self.cliente.pk]),
            {'nome': 'João Editado', 'cpf': '987.654.321-00', 'email': 'joao@email.com', 'telefone': '', 'endereco': ''},
        )
        self.assertEqual(response.status_code, 302)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.nome, 'João Editado')

    def test_excluir(self):
        response = self.client.post(reverse('excluir_cliente', args=[self.cliente.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cliente.objects.count(), 0)
