"""
Módulo para coleta de telemetria.
"""
import psutil
from datetime import datetime, timezone


class ColetorTelemetria:
    """Classe responsável por coletar telemetria do sistema"""
    
    @staticmethod
    def obter_percentual_cpu():
        """Obtém o percentual de utilização da CPU"""
        return psutil.cpu_percent(interval=1)
    
    @staticmethod
    def obter_ram_utilizada():
        """Obtém a quantidade de RAM utilizada em GB"""
        memoria = psutil.virtual_memory()
        return round(memoria.used / (1024 ** 3), 2)
    
    @staticmethod
    def obter_percentual_ram():
        """Obtém o percentual de utilização de RAM"""
        return psutil.virtual_memory().percent
    
    @staticmethod
    def obter_timestamp_utc():
        """Obtém o timestamp atual em UTC no formato ISO"""
        return datetime.now(timezone.utc).isoformat()
    
    @staticmethod
    def coletar_telemetria():
        """Coleta uma amostra completa de telemetria"""
        return {
            'percentual_uso_cpu': ColetorTelemetria.obter_percentual_cpu(),
            'ram_utilizada_gb': ColetorTelemetria.obter_ram_utilizada(),
            'coletado_em': ColetorTelemetria.obter_timestamp_utc(),
        }
