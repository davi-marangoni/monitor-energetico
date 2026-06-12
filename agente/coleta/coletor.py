from datetime import datetime, UTC
import platform
import socket
from pathlib import Path

import psutil


class ColetorSistema:
    @staticmethod
    def coletar_identificacao_maquina():
        machine_id = Path("/etc/machine-id").read_text(encoding="utf-8").strip()
        memoria = psutil.virtual_memory()
        return {
            "hostname": socket.gethostname(),
            "machine_id_linux": machine_id,
            "modelo_cpu": platform.processor() or "desconhecido",
            "total_ram_gb": round(memoria.total / (1024 ** 3), 2),
            "nome_sistema_operacional": platform.system(),
            "versao_sistema_operacional": platform.release(),
        }

    @staticmethod
    def coletar_telemetria():
        memoria = psutil.virtual_memory()
        return {
            "percentual_uso_cpu": psutil.cpu_percent(interval=None),
            "ram_utilizada_gb": round(memoria.used / (1024 ** 3), 3),
            "coletado_em": datetime.now(UTC).isoformat(),
        }
