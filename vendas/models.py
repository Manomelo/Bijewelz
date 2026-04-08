from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from produtos.models import Produto


class Venda(models.Model):
    data        = models.DateField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cliente     = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    usuario     = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = 'vendas'
        ordering = ['-data']

    def __str__(self):
        return f'Venda #{self.id} - {self.cliente.nome}'

    def calcular_total(self):
        total = sum(item.calcular_subtotal() for item in self.itens.all())
        self.valor_total = total
        self.save()


class ItemVenda(models.Model):
    venda          = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto        = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade     = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'itens_venda'

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'

    def calcular_subtotal(self):
        return self.quantidade * self.preco_unitario