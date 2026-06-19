from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import Telemetria
from .serializers import (
    TelemetriaSerializer,
    TelemetriaCriacaoSerializer,
    TelemetriaLoteSerializer,
)
from aplicativos.maquinas.models import Maquina
from aplicativos.energia.servicos.servico_dashboard import serializar_telemetria_com_consumo


class TelemetriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para gerenciar telemetrias
    
    GET /api/telemetrias - Lista telemetrias do usuário
    GET /api/telemetrias/{id} - Detalha uma telemetria específica
    POST /api/telemetrias/lote - Envia lote de telemetrias (via agente)
    """
    serializer_class = TelemetriaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas telemetrias das máquinas do usuário"""
        return Telemetria.objects.filter(
            maquina__usuario=self.request.user
        ).order_by('-coletado_em')
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def lote(self, request):
        """
        POST /api/telemetrias/lote
        Envia um lote de telemetrias do agente
        
        Formato esperado:
        {
            "machine_id": "abc123",
            "telemetrias": [
                {
                    "percentual_uso_cpu": 35.5,
                    "ram_utilizada_gb": 8.2,
                    "coletado_em": "2026-06-01T10:00:00Z"
                }
            ]
        }
        """
        serializer = TelemetriaLoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            maquina = Maquina.objects.get(
                machine_id_linux=serializer.validated_data['machine_id'],
                usuario=request.user
            )
        except Maquina.DoesNotExist:
            return Response(
                {'erro': 'Máquina não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        telemetrias_data = serializer.validated_data['telemetrias']
        telemetrias_criadas = []
        
        for telemetria_data in telemetrias_data:
            try:
                telemetria = Telemetria.objects.create(
                    maquina=maquina,
                    percentual_uso_cpu=float(telemetria_data['percentual_uso_cpu']),
                    ram_utilizada_gb=float(telemetria_data['ram_utilizada_gb']),
                    coletado_em=telemetria_data['coletado_em']
                )
                telemetrias_criadas.append(telemetria)
            except (ValueError, KeyError) as e:
                return Response(
                    {'erro': f'Erro ao processar telemetria: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Atualiza o último ping da máquina
        maquina.ultimo_ping_em = timezone.now()
        maquina.save()
        
        return Response(
            {
                'mensagem': f'{len(telemetrias_criadas)} telemetrias recebidas com sucesso',
                'quantidade': len(telemetrias_criadas)
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def historico(self, request):
        """
        GET /api/telemetrias/historico?filtro=ultima_hora
        
        Filtros suportados:
        - ultima_hora: últimas telemetrias da última hora
        - ultimas_24_horas: últimas 24 horas
        - ultimos_7_dias: últimos 7 dias
        - ultimos_30_dias: últimos 30 dias
        - personalizado: com data_inicio e data_fim
        """
        filtro = request.query_params.get('filtro', 'ultimas_24_horas')
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        maquina_id = request.query_params.get('maquina_id')
        
        agora = timezone.now()
        
        if filtro == 'ultima_hora':
            data_inicio = agora - timedelta(hours=1)
        elif filtro == 'ultimas_24_horas':
            data_inicio = agora - timedelta(hours=24)
        elif filtro == 'ultimos_7_dias':
            data_inicio = agora - timedelta(days=7)
        elif filtro == 'ultimos_30_dias':
            data_inicio = agora - timedelta(days=30)
        elif filtro == 'personalizado':
            if not data_inicio or not data_fim:
                return Response(
                    {'erro': 'data_inicio e data_fim são obrigatórios para filtro personalizado'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            data_inicio = agora - timedelta(hours=24)
        
        queryset = self.get_queryset()

        if maquina_id:
            queryset = queryset.filter(maquina_id=maquina_id)
        
        if data_inicio:
            queryset = queryset.filter(coletado_em__gte=data_inicio)
        if data_fim and filtro == 'personalizado':
            queryset = queryset.filter(coletado_em__lte=data_fim)
        
        dados = [serializar_telemetria_com_consumo(item) for item in queryset]
        return Response(dados)
