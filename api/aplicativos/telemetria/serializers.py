from rest_framework import serializers
from .models import Telemetria


class TelemetriaSerializer(serializers.ModelSerializer):
    """Serializer para telemetria"""
    
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


class TelemetriaLoteSerializer(serializers.Serializer):
    """Serializer para lote de telemetrias enviadas pelo agente"""
    
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
