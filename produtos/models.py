from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    imagem = models.ImageField(upload_to='categorias/', blank=True, null=True)

    class Meta:
        db_table = 'categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    qtd_estoque = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = 'produtos'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def tem_estoque(self, quantidade):
        return self.qtd_estoque >= quantidade

    def estoque_baixo(self):
        return self.qtd_estoque <= self.estoque_minimo