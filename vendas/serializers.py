from rest_framework import serializers
from .models import Venda, ItemVenda
from produtos.serializer import ProdutoSerializer

class ItemVendaSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    produto_detalhe = ProdutoSerializer(source='produto', read_only=True)

    class Meta:
        model = ItemVenda
        fields = [
            'id',
            'produto',
            'produto_detalhe',
            'quantidade',
            'preco_unitario',
            'subtotal'
        ]

class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True, read_only=True)

    class Meta:
        model = Venda
        fields = [
            'id',
            'cliente',
            'data_venda',
            'total',
            'itens'
        ]

        