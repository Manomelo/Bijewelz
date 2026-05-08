from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_vendas, name='listar_vendas'),
    path('nova/', views.nova_venda, name='nova_venda'),
    path('<int:pk>/', views.detalhe_venda, name='detalhe_venda'),
]
