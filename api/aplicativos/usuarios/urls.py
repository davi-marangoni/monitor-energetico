from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UsuarioCadastroView, UsuarioAtualView

urlpatterns = [
    # Autenticação JWT
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Usuário
    path('cadastro', UsuarioCadastroView.as_view(), name='usuario_cadastro'),
    path('me', UsuarioAtualView.as_view(), name='usuario_atual'),
]
