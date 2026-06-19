from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .servicos.servico_dashboard import (
    obter_consumo_geral,
    obter_ranking_maquinas,
    obter_resumo_dashboard,
)


class DashboardResumoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(obter_resumo_dashboard(request.user))


class DashboardRankingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        top, ranking = obter_ranking_maquinas(request.user)
        return Response({'top': top, 'ranking': ranking})


class DashboardConsumoGeralView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filtro = request.query_params.get('filtro', 'ultimas_24_horas')
        return Response(obter_consumo_geral(request.user, filtro))
