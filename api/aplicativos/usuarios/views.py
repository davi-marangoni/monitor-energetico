from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from .serializers import UsuarioCadastroSerializer, UsuarioSerializer


class UsuarioCadastroView(generics.CreateAPIView):
    """
    POST /api/autenticacao/cadastro
    Registra um novo usuário no sistema
    """
    queryset = User.objects.all()
    serializer_class = UsuarioCadastroSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'mensagem': 'Usuário cadastrado com sucesso'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UsuarioAtualView(generics.RetrieveAPIView):
    """
    GET /api/autenticacao/me
    Retorna os dados do usuário autenticado atualmente
    """
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
