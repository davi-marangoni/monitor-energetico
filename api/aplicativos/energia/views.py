from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ConfiguracaoEnergetica
from .serializers import ConfiguracaoEnergeticaSerializer


class ConfiguracaoEnergeticaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar configurações energéticas
    
    GET /api/configuracoes-energeticas - Lista configurações do usuário
    POST /api/configuracoes-energeticas - Cria nova configuração
    GET /api/configuracoes-energeticas/{id} - Detalha uma configuração
    PATCH /api/configuracoes-energeticas/{id} - Atualiza uma configuração
    """
    serializer_class = ConfiguracaoEnergeticaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas configurações das máquinas do usuário"""
        return ConfiguracaoEnergetica.objects.filter(
            maquina__usuario=self.request.user
        )
    
    def perform_create(self, serializer):
        """Valida que a máquina pertence ao usuário"""
        maquina = serializer.validated_data.get('maquina')
        if maquina.usuario != self.request.user:
            raise PermissionError('Você não tem permissão para esta máquina')
        serializer.save()
