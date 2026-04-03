from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    qtd_estoque = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=0)

    class Meta:
        db_table = 'produtos'
        ordering = ['nome']

    def __str__(self):
        return self.nome
    
    def tem_estoque(self, quantidade):
        return self.qtd_estoque >= quantidade
    
    def estoque_baixo(self):
        return self.qtd_estoque <= self.estoque_minimo