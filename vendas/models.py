from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from produtos.models import Produto


class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_venda = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'vendas'
        ordering = ['-data_venda']

    def __str__(self):
        return f'Venda #{self.pk}'


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'itens_venda'

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

class Carrinho(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrinho')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carrinhos'

    def __str__(self):
        return f'Carrinho de {self.usuario.username}'

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'itens_carrinho'
        unique_together = ('carrinho', 'produto')

    def subtotal(self):
        return self.quantidade * self.produto.preco
