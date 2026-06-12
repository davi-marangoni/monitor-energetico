from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from aplicativos.energia.models import ConfiguracaoEnergetica
from aplicativos.energia.serializers import ConfiguracaoEnergeticaSerializer
from aplicativos.maquinas.models import Maquina


class ConfiguracaoEnergeticaListarCriarView(APIView):
    def get(self, request):
        configs = ConfiguracaoEnergetica.objects.filter(maquina__usuario=request.user).order_by("-atualizado_em")
        return Response(ConfiguracaoEnergeticaSerializer(configs, many=True).data)

    def post(self, request):
        maquina = Maquina.objects.filter(id=request.data.get("maquina"), usuario=request.user).first()
        if not maquina:
            return Response({"erro": "Máquina não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        ConfiguracaoEnergetica.objects.filter(maquina=maquina, ativo=True).update(ativo=False)
        serializer = ConfiguracaoEnergeticaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(ativo=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConfiguracaoEnergeticaDetalheView(APIView):
    def patch(self, request, id):
        config = ConfiguracaoEnergetica.objects.filter(id=id, maquina__usuario=request.user).first()
        if not config:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ConfiguracaoEnergeticaSerializer(config, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
