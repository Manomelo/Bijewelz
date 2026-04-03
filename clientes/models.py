from django.db import models

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.TextField(blank=True)

    class Meta:
        db_table = 'clientes'
        ordering = ['nome']

        def __str__(self):
            return self.nome