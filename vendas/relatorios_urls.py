from django.urls import path
from . import views

urlpatterns = [
    path('', views.relatorio_vendas, name='relatorio_vendas'),
]
