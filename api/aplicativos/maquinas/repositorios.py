from django.utils import timezone

from aplicativos.maquinas.models import Maquina


class RepositorioMaquinas:
    @staticmethod
    def listar_por_usuario(usuario):
        return Maquina.objects.filter(usuario=usuario).order_by("hostname")

    @staticmethod
    def obter_por_id_usuario(id_maquina, usuario):
        return Maquina.objects.filter(id=id_maquina, usuario=usuario).first()

    @staticmethod
    def obter_por_machine_id(machine_id_linux):
        return Maquina.objects.filter(machine_id_linux=machine_id_linux).first()

    @staticmethod
    def atualizar_ping(maquina):
        maquina.ultimo_ping_em = timezone.now()
        maquina.save(update_fields=["ultimo_ping_em", "atualizado_em"])
