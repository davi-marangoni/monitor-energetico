from aplicativos.usuarios.serializers import CadastroUsuarioSerializer


class ServicoCadastroUsuario:
    @staticmethod
    def cadastrar(dados):
        serializer = CadastroUsuarioSerializer(data=dados)
        serializer.is_valid(raise_exception=True)
        return serializer.save()
