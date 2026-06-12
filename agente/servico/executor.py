import time

from cliente_api.cliente import ClienteApiMonitor
from coleta.coletor import ColetorSistema
from configuracao.config import ConfiguracaoAgente
from fila_local.repositorio_fila import RepositorioFilaLocal


class ExecutorServicoAgente:
    def __init__(self):
        self.config = ConfiguracaoAgente()
        self.fila = RepositorioFilaLocal()
        self.cliente = ClienteApiMonitor(self.config.api_url, self.config.usuario, self.config.senha)
        self.maquina = ColetorSistema.coletar_identificacao_maquina()
        self.dados_maquina = self.cliente.registrar_maquina(
            {
                **self.maquina,
                "intervalo_coleta_segundos": self.config.intervalo_coleta_padrao,
                "intervalo_envio_segundos": self.config.intervalo_envio_padrao,
            }
        )

    def executar(self):
        proxima_coleta = 0
        proximo_envio = 0
        while True:
            agora = time.time()
            if agora >= proxima_coleta:
                self.fila.enfileirar(ColetorSistema.coletar_telemetria())
                proxima_coleta = agora + self.dados_maquina.get("intervalo_coleta_segundos", self.config.intervalo_coleta_padrao)

            if agora >= proximo_envio:
                pendencias = self.fila.listar()
                if pendencias:
                    payload = [item["payload"] for item in pendencias]
                    self.cliente.enviar_lote_telemetria(self.maquina["machine_id_linux"], payload)
                    self.fila.remover([item["id"] for item in pendencias])
                proximo_envio = agora + self.dados_maquina.get("intervalo_envio_segundos", self.config.intervalo_envio_padrao)

            time.sleep(1)
