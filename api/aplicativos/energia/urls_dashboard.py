from django.urls import path

from .views_dashboard import (
    DashboardConsumoGeralView,
    DashboardRankingView,
    DashboardResumoView,
)

urlpatterns = [
    path('resumo/', DashboardResumoView.as_view(), name='dashboard_resumo'),
    path('ranking/', DashboardRankingView.as_view(), name='dashboard_ranking'),
    path('consumo-geral/', DashboardConsumoGeralView.as_view(), name='dashboard_consumo_geral'),
]
