from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TelemetriaViewSet

router = DefaultRouter()
router.register(r'', TelemetriaViewSet, basename='telemetria')

urlpatterns = [
    path('', include(router.urls)),
]
