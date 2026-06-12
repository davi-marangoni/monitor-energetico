from rest_framework import serializers
from .models import Maquina


class MaquinaRegistroSerializer(serializers.ModelSerializer):
    """Serializer para registro/atualização de máquina pelo agente"""
    
    class Meta:
        model = Maquina
        fields = [
            'hostname',
            'machine_id_linux',
            'modelo_cpu',
            'total_ram_gb',
            'nome_sistema_operacional',
            'versao_sistema_operacional',
            'intervalo_coleta_segundos',
            'intervalo_envio_segundos',
        ]
        read_only_fields = []


class MaquinaSerializer(serializers.ModelSerializer):
    """Serializer para exibição de máquina"""
    
    class Meta:
        model = Maquina
        fields = [
            'id',
            'hostname',
            'machine_id_linux',
            'modelo_cpu',
            'total_ram_gb',
            'nome_sistema_operacional',
            'versao_sistema_operacional',
            'intervalo_coleta_segundos',
            'intervalo_envio_segundos',
            'ativo',
            'ultimo_ping_em',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class MaquinaAtualizacaoSerializer(serializers.ModelSerializer):
    """Serializer para atualização de máquina"""
    
    class Meta:
        model = Maquina
        fields = [
            'intervalo_coleta_segundos',
            'intervalo_envio_segundos',
            'ativo',
        ]
