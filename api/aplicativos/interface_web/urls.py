from django.urls import path

from .views import (
    CadastroView,
    CustomLoginView,
    CustomLogoutView,
    PerfilView,
    configuracao_energetica_view,
    configuracoes_global_view,
    dashboard_view,
    maquina_detail_view,
    maquina_edit_view,
    maquinas_list_view,
)

urlpatterns = [
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', CustomLogoutView.as_view(), name='logout'),
    path('cadastro', CadastroView.as_view(), name='cadastro'),
    path('', dashboard_view, name='dashboard'),
    path('maquinas', maquinas_list_view, name='maquinas_list'),
    path('maquinas/<int:pk>/', maquina_detail_view, name='maquina_detail'),
    path('maquinas/<int:pk>/editar', maquina_edit_view, name='maquina_edit'),
    path('maquinas/<int:pk>/configuracao', configuracao_energetica_view, name='maquina_configuracao'),
    path('configuracoes', configuracoes_global_view, name='configuracoes_global'),
    path('perfil', PerfilView.as_view(), name='perfil'),
]
