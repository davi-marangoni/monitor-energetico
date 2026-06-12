from rest_framework import serializers

from aplicativos.maquinas.models import Maquina


class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = [
            "id",
            "hostname",
            "machine_id_linux",
            "modelo_cpu",
            "total_ram_gb",
            "nome_sistema_operacional",
            "versao_sistema_operacional",
            "intervalo_coleta_segundos",
            "intervalo_envio_segundos",
            "ativo",
            "ultimo_ping_em",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["id", "criado_em", "atualizado_em", "ultimo_ping_em"]


class MaquinaRegistroSerializer(MaquinaSerializer):
    class Meta(MaquinaSerializer.Meta):
        read_only_fields = ["id", "criado_em", "atualizado_em", "ultimo_ping_em"]
