from django.utils import timezone

from aplicativos.maquinas.repositorios import RepositorioMaquinas
from aplicativos.maquinas.serializers import MaquinaRegistroSerializer


class ServicoRegistroMaquina:
    @staticmethod
    def registrar_ou_atualizar(usuario, dados):
        machine_id = dados.get("machine_id_linux")
        maquina = RepositorioMaquinas.obter_por_machine_id(machine_id)

        if maquina and maquina.usuario_id != usuario.id:
            raise ValueError("machine_id_linux já cadastrado para outro usuário")

        if maquina:
            serializer = MaquinaRegistroSerializer(maquina, data=dados, partial=True)
        else:
            serializer = MaquinaRegistroSerializer(data=dados)

        serializer.is_valid(raise_exception=True)
        maquina = serializer.save(usuario=usuario, ultimo_ping_em=timezone.now())
        return maquina
