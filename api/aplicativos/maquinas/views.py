from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from aplicativos.maquinas.repositorios import RepositorioMaquinas
from aplicativos.maquinas.serializers import MaquinaSerializer
from aplicativos.maquinas.servicos import ServicoRegistroMaquina


class MaquinaListarView(APIView):
    def get(self, request):
        maquinas = RepositorioMaquinas.listar_por_usuario(request.user)
        return Response(MaquinaSerializer(maquinas, many=True).data)


class MaquinaRegistrarView(APIView):
    def post(self, request):
        try:
            maquina = ServicoRegistroMaquina.registrar_ou_atualizar(request.user, request.data)
        except ValueError as erro:
            return Response({"erro": str(erro)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MaquinaSerializer(maquina).data, status=status.HTTP_201_CREATED)


class MaquinaDetalheAtualizacaoView(APIView):
    def get(self, request, id):
        maquina = RepositorioMaquinas.obter_por_id_usuario(id, request.user)
        if not maquina:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(MaquinaSerializer(maquina).data)

    def patch(self, request, id):
        maquina = RepositorioMaquinas.obter_por_id_usuario(id, request.user)
        if not maquina:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MaquinaSerializer(maquina, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
