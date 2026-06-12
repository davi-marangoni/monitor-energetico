from rest_framework import serializers

from aplicativos.energia.models import ConfiguracaoEnergetica


class ConfiguracaoEnergeticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoEnergetica
        fields = [
            "id",
            "maquina",
            "tdp_cpu_watts",
            "fator_idle_alpha",
            "consumo_ram_por_gb",
            "ativo",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["id", "criado_em", "atualizado_em"]
