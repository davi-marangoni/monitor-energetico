from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConfiguracaoEnergeticaViewSet

router = DefaultRouter()
router.register(r'', ConfiguracaoEnergeticaViewSet, basename='configuracao_energetica')

urlpatterns = [
    path('', include(router.urls)),
]
