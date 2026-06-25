from rest_framework import serializers
from .models import Produto

class ProdutoSerializer(serializers.ModelSerializer):
    estoque_baixo = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = [
            'id',
            'nome',
            'descricao',
            'preco',
            'qtd_estoque',
            'estoque_minimo',
            'estoque_baixo'
        ]

    def get_estoque_baixo(self, obj):
        return obj.estoque_baixo()