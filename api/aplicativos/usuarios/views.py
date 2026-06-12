from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from aplicativos.usuarios.serializers import UsuarioAtualSerializer
from aplicativos.usuarios.servicos import ServicoCadastroUsuario


class AutenticacaoCadastroView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        usuario = ServicoCadastroUsuario.cadastrar(request.data)
        return Response(UsuarioAtualSerializer(usuario).data, status=status.HTTP_201_CREATED)


class AutenticacaoMeView(APIView):
    def get(self, request):
        return Response(UsuarioAtualSerializer(request.user).data)
