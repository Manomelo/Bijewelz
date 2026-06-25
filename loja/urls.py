from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='loja_inicio'),
    path('produtos/', views.listar_produtos, name='loja_produtos'),
    path('produtos/<int:pk>/', views.detalhe_produto, name='loja_detalhe_produto'),
    path('carrinho/', views.ver_carrinho, name='loja_carrinho'),
    path('carrinho/adicionar/<int:pk>/', views.adicionar_ao_carrinho, name='loja_adicionar_carrinho'),
    path('carrinho/remover/<int:pk>/', views.remover_do_carrinho, name='loja_remover_carrinho'),
    path('conta/login/', views.login_view, name='loja_login'),
    path('conta/registro/', views.registro_view, name='loja_registro'),
    path('conta/logout/', views.logout_view, name='loja_logout'),
    path('finalizar/', views.finalizar_pedido, name='loja_finalizar'),
    path('pedido/<int:pk>/', views.pedido_confirmado, name='loja_pedido_confirmado'),
]