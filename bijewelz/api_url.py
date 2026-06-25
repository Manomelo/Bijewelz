from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from produtos.api_views import ProdutoViewSet
from clientes.api_views import ClienteViewSet
from vendas.api_views import VendaViewSet
from django.urls import path

router = DefaultRouter()
router.register('produtos', ProdutoViewSet)
router.register('clientes', ClienteViewSet)
router.register('vendas', VendaViewSet, basename='venda')


urlpatterns = [
    *router.urls,
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]