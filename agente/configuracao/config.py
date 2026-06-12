from dataclasses import dataclass
import os


@dataclass
class ConfiguracaoAgente:
    api_url: str = os.getenv("API_URL", "http://localhost:8000/api")
    usuario: str = os.getenv("AGENTE_USUARIO", "")
    senha: str = os.getenv("AGENTE_SENHA", "")
    intervalo_coleta_padrao: int = int(os.getenv("INTERVALO_COLETA", "10"))
    intervalo_envio_padrao: int = int(os.getenv("INTERVALO_ENVIO", "60"))
