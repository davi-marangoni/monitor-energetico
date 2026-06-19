from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Maquina
from .serializers import (
    MaquinaRegistroSerializer,
    MaquinaSerializer,
    MaquinaAtualizacaoSerializer,
)


class MaquinaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar máquinas
    
    GET /api/maquinas - Lista todas as máquinas do usuário
    POST /api/maquinas/registrar - Registra uma nova máquina (via agente)
    GET /api/maquinas/{id} - Detalha uma máquina específica
    PATCH /api/maquinas/{id} - Atualiza uma máquina específica
    """
    serializer_class = MaquinaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas as máquinas do usuário autenticado"""
        queryset = Maquina.objects.filter(usuario=self.request.user)
        machine_id_linux = self.request.query_params.get('machine_id_linux')
        if machine_id_linux:
            queryset = queryset.filter(machine_id_linux=machine_id_linux)
        return queryset
    
    def perform_create(self, serializer):
        """Associa a máquina ao usuário autenticado"""
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def registrar(self, request):
        """
        POST /api/maquinas/registrar
        Registra ou atualiza uma máquina pelo agente
        """
        serializer = MaquinaRegistroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        machine_id = serializer.validated_data.get('machine_id_linux')
        
        # Procura a máquina existente ou cria uma nova
        maquina, created = Maquina.objects.update_or_create(
            machine_id_linux=machine_id,
            defaults={
                **serializer.validated_data,
                'usuario': request.user,
                'ultimo_ping_em': timezone.now(),
            }
        )
        
        output_serializer = MaquinaSerializer(maquina)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        return Response(output_serializer.data, status=status_code)
    
    def get_serializer_class(self):
        """Define qual serializer usar baseado na ação"""
        if self.action == 'registrar':
            return MaquinaRegistroSerializer
        elif self.action in ['partial_update', 'update']:
            return MaquinaAtualizacaoSerializer
        return MaquinaSerializer
    
    def partial_update(self, request, *args, **kwargs):
        """Atualiza parcialmente uma máquina"""
        maquina = self.get_object()
        serializer = self.get_serializer(maquina, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(MaquinaSerializer(maquina).data)
