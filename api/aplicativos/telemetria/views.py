from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from aplicativos.telemetria.serializers import TelemetriaLoteEntradaSerializer, TelemetriaSerializer
from aplicativos.telemetria.servicos import ServicoTelemetria


class TelemetriaLoteView(APIView):
    def post(self, request):
        serializer = TelemetriaLoteEntradaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            quantidade = ServicoTelemetria.salvar_lote(
                request.user,
                serializer.validated_data["machine_id"],
                serializer.validated_data["telemetrias"],
            )
        except ValueError as erro:
            return Response({"erro": str(erro)}, status=status.HTTP_404_NOT_FOUND)
        return Response({"recebidas": quantidade}, status=status.HTTP_201_CREATED)


class TelemetriaListarView(APIView):
    def get(self, request):
        telemetrias = ServicoTelemetria.listar(request.user, request.query_params.get("maquina_id"))[:1000]
        return Response(TelemetriaSerializer(telemetrias, many=True).data)


class TelemetriaHistoricoView(APIView):
    def get(self, request):
        historico = ServicoTelemetria.historico_com_consumo(
            usuario=request.user,
            periodo=request.query_params.get("periodo"),
            inicio=request.query_params.get("inicio"),
            fim=request.query_params.get("fim"),
            maquina_id=request.query_params.get("maquina_id"),
        )
        return Response(historico)
