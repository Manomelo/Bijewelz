from rest_framework.test import APITestCase
from .models import Cliente

class ClienteAPITest(APITestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Lucas Melo",
            cpf="123.456.789-00",
            email="lucas@email.com",
            telefone = "619999999999",
        )

    def test_listar_clientes(self):
        response = self.client.get('/api/clientes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_detalhe_cliente(self):
        response = self.client.get(f'/api/clientes/{self.cliente.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nome'], 'Lucas Melo')
        self.assertEqual(response.data['cpf'], '123.456.789-00')

    def test_criar_cliente(self):
        response = self.client.post('/api/clientes/', {
            'nome': 'João Santos',
            'cpf': '987.654.321-00',
            'email': 'joao@email.com',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_editar_cliente(self):
        response = self.client.put(f'/api/clientes/{self.cliente.pk}/', {
            'nome': 'Lucas Editado',
            'cpf': '123.456.789-00',
            'email': 'lucas@email.com',
        })
        self.assertEqual(response.status_code, 200)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.nome, 'Lucas Editado')

    def test_excluir_cliente(self):
        response = self.client.delete(f'/api/clientes/{self.cliente.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Cliente.objects.count(), 0)

    def test_criar_cliente_cpf_duplicado(self):
        response = self.client.post('/api/clientes/', {
            'nome': 'Clone',
            'cpf': '123.456.789-00',
            'email': 'clone@email.com',
        })
        self.assertEqual(response.status_code, 400)

    def test_detalhe_cliente_inexistente(self):
        response = self.client.get('/api/clientes/9999/')
        self.assertEqual(response.status_code, 404)