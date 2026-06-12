from rest_framework import serializers

from aplicativos.telemetria.models import Telemetria


class TelemetriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telemetria
        fields = ["id", "maquina", "percentual_uso_cpu", "ram_utilizada_gb", "coletado_em", "criado_em"]
        read_only_fields = ["id", "criado_em"]


class TelemetriaLoteEntradaSerializer(serializers.Serializer):
    machine_id = serializers.CharField()
    telemetrias = serializers.ListField(child=serializers.DictField(), allow_empty=False)
