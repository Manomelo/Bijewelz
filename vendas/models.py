from django.db import models
from clientes.models import Cliente
from produtos.models import Produto


class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
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
