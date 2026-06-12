from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaquinaViewSet

router = DefaultRouter()
router.register(r'', MaquinaViewSet, basename='maquina')

urlpatterns = [
    path('', include(router.urls)),
]
