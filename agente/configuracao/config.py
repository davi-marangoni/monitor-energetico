"""
Configuração do agente de monitoramento.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Configuracao:
    """Classe de configuração do agente"""
    
    # API Configuration
    API_URL = os.getenv('API_URL', 'http://localhost:8000/api')
    API_USERNAME = os.getenv('API_USERNAME', '')
    API_PASSWORD = os.getenv('API_PASSWORD', '')
    API_TOKEN = os.getenv('API_TOKEN', '')
    
    # Intervals (in seconds)
    INTERVALO_COLETA = int(os.getenv('INTERVALO_COLETA', 60))  # 1 minute
    INTERVALO_ENVIO = int(os.getenv('INTERVALO_ENVIO', 300))   # 5 minutes
    
    # Local queue database
    FILA_DB_PATH = os.getenv('FILA_DB_PATH', '/var/lib/monitor-energetico/fila.db')
    
    # Service configuration
    SERVICE_NAME = 'monitor-energetico'
    SERVICE_PATH = '/etc/systemd/system/monitor-energetico.service'
    INSTALL_PATH = '/opt/monitor-energetico'
    
    # Logging
    LOG_PATH = os.getenv('LOG_PATH', '/var/log/monitor-energetico')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def validar():
        """Valida as configurações necessárias"""
        if not Configuracao.API_URL:
            raise ValueError('API_URL é obrigatória')
        
        if not (Configuracao.API_USERNAME and Configuracao.API_PASSWORD) and not Configuracao.API_TOKEN:
            raise ValueError('Credenciais de API são obrigatórias (username/password ou token)')
        
        return True
