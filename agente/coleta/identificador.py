"""
Módulo para identificação da máquina.
"""
import socket
import platform
import psutil
import os


class IdentificadorMaquina:
    """Classe responsável por identificar a máquina"""
    
    @staticmethod
    def obter_hostname():
        """Obtém o hostname da máquina"""
        return socket.gethostname()
    
    @staticmethod
    def obter_machine_id():
        """Obtém o ID da máquina do Linux"""
        try:
            with open('/etc/machine-id', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback para UUID
            import uuid
            return str(uuid.getnode())
    
    @staticmethod
    def obter_sistema_operacional():
        """Obtém o nome do sistema operacional"""
        return platform.system()
    
    @staticmethod
    def obter_versao_so():
        """Obtém a versão do sistema operacional"""
        return platform.release()
    
    @staticmethod
    def obter_processador():
        """Obtém informações do processador"""
        try:
            # Tenta usar lscpu primeiro
            import subprocess
            resultado = subprocess.run(['lscpu'], capture_output=True, text=True, timeout=5)
            if resultado.returncode == 0:
                for linha in resultado.stdout.split('\n'):
                    if 'Model name' in linha:
                        return linha.split(':', 1)[1].strip()
        except Exception:
            pass
        
        # Fallback para platform.processor()
        return platform.processor()
    
    @staticmethod
    def obter_total_ram():
        """Obtém a quantidade total de RAM em GB"""
        return round(psutil.virtual_memory().total / (1024 ** 3), 2)
    
    @staticmethod
    def obter_informacoes_completas():
        """Obtém todas as informações da máquina"""
        return {
            'hostname': IdentificadorMaquina.obter_hostname(),
            'machine_id_linux': IdentificadorMaquina.obter_machine_id(),
            'modelo_cpu': IdentificadorMaquina.obter_processador(),
            'total_ram_gb': IdentificadorMaquina.obter_total_ram(),
            'nome_sistema_operacional': IdentificadorMaquina.obter_sistema_operacional(),
            'versao_sistema_operacional': IdentificadorMaquina.obter_versao_so(),
        }
