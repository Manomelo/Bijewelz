from django.core.serializers import serialize
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from  django.shortcuts import get_object_or_404
from .models import Venda
from .serializers import VendaSerializer

class VendaViewSet(ViewSet):
    def list(self, request):
        vendas = Venda.objects.all()
        serializer = VendaSerializer(vendas, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        venda = get_object_or_404(Venda, pk=pk)
        serializer = VendaSerializer(venda)
        return Response(serializer.data)