from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_produtos, name='listar_produtos'),
    path('novo/', views.criar_produto, name='criar_produto'),
    path('<int:pk>/editar/', views.editar_produto, name='editar_produto'),
    path('<int:pk>/excluir/', views.excluir_produto, name='excluir_produto'),
    path('<int:pk>/ativar/', views.ativar_produto, name='ativar_produto'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/nova/', views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/excluir/', views.excluir_categoria, name='excluir_categoria'),
]