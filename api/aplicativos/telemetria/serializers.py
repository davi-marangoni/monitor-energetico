from rest_framework import serializers
from .models import Telemetria


class TelemetriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telemetria
        fields = [
            'id',
            'maquina',
            'percentual_uso_cpu',
            'ram_utilizada_gb',
            'coletado_em',
            'criado_em',
        ]
        read_only_fields = ['id', 'criado_em']


class TelemetriaComConsumoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    maquina = serializers.IntegerField()
    percentual_uso_cpu = serializers.FloatField()
    ram_utilizada_gb = serializers.FloatField()
    coletado_em = serializers.DateTimeField()
    criado_em = serializers.DateTimeField()
    consumo_cpu = serializers.FloatField()
    consumo_ram = serializers.FloatField()
    consumo_total = serializers.FloatField()


class TelemetriaLoteSerializer(serializers.Serializer):
    machine_id = serializers.CharField()
    telemetrias = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )


class TelemetriaCriacaoSerializer(serializers.ModelSerializer):
    """Serializer para criação de telemetria"""
    
    class Meta:
        model = Telemetria
        fields = [
            'percentual_uso_cpu',
            'ram_utilizada_gb',
            'coletado_em',
        ]
