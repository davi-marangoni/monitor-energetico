"""
Serviço principal do agente de monitoramento.
"""
import logging
import threading
import time
from datetime import datetime

from configuracao.config import Configuracao
from coleta.identificador import IdentificadorMaquina
from coleta.coletor import ColetorTelemetria
from cliente_api.cliente import ClienteAPI
from fila_local.fila import FilaLocal


# Configurar logging
logging.basicConfig(
    level=Configuracao.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class ServicoAgente:
    """Serviço principal do agente de monitoramento"""
    
    def __init__(self):
        """Inicializa o serviço"""
        self.logger = logging.getLogger(__name__)
        self.em_execucao = False
        
        # Validar configurações
        Configuracao.validar()
        
        # Inicializar componentes
        self.fila = FilaLocal(Configuracao.FILA_DB_PATH)
        self.cliente_api = ClienteAPI(
            Configuracao.API_URL,
            username=Configuracao.API_USERNAME,
            password=Configuracao.API_PASSWORD,
            token=Configuracao.API_TOKEN
        )
        
        # Informações da máquina
        self.infos_maquina = IdentificadorMaquina.obter_informacoes_completas()
        self.machine_id = self.infos_maquina['machine_id_linux']
        
        self.logger.info(f'Agente inicializado para máquina: {self.infos_maquina["hostname"]}')
    
    def iniciar(self):
        """Inicia o serviço do agente"""
        self.logger.info('Iniciando agente de monitoramento...')
        self.em_execucao = True
        
        # Tentar registrar a máquina
        try:
            self.cliente_api.registrar_maquina({
                **self.infos_maquina,
                'intervalo_coleta_segundos': Configuracao.INTERVALO_COLETA,
                'intervalo_envio_segundos': Configuracao.INTERVALO_ENVIO,
            })
        except Exception as e:
            self.logger.error(f'Erro ao registrar máquina: {str(e)}')
        
        # Iniciar ciclos
        thread_coleta = threading.Thread(target=self._ciclo_coleta, daemon=True)
        thread_envio = threading.Thread(target=self._ciclo_envio, daemon=True)
        
        thread_coleta.start()
        thread_envio.start()
        
        # Manter o serviço rodando
        try:
            while self.em_execucao:
                time.sleep(1)
        except KeyboardInterrupt:
            self.parar()
    
    def _ciclo_coleta(self):
        """Ciclo de coleta de telemetrias"""
        self.logger.info('Ciclo de coleta iniciado')
        
        while self.em_execucao:
            try:
                # Coletar telemetria
                telemetria = ColetorTelemetria.coletar_telemetria()
                
                # Adicionar à fila local
                self.fila.adicionar_telemetria(self.machine_id, telemetria)
                
                self.logger.debug(f'Telemetria coletada: CPU={telemetria["percentual_uso_cpu"]}% RAM={telemetria["ram_utilizada_gb"]}GB')
                
            except Exception as e:
                self.logger.error(f'Erro no ciclo de coleta: {str(e)}')
            
            # Aguardar próximo ciclo
            time.sleep(Configuracao.INTERVALO_COLETA)
    
    def _ciclo_envio(self):
        """Ciclo de envio de telemetrias"""
        self.logger.info('Ciclo de envio iniciado')
        
        while self.em_execucao:
            try:
                # Obter telemetrias pendentes
                pendentes = self.fila.obter_pendentes(self.machine_id)
                
                if pendentes:
                    # Preparar dados para envio
                    telemetrias = []
                    ids_enviadas = []
                    
                    for telemetria in pendentes:
                        telemetrias.append({
                            'percentual_uso_cpu': telemetria['percentual_uso_cpu'],
                            'ram_utilizada_gb': telemetria['ram_utilizada_gb'],
                            'coletado_em': telemetria['coletado_em']
                        })
                        ids_enviadas.append(telemetria['id'])
                    
                    # Enviar para a API
                    try:
                        self.cliente_api.enviar_lote_telemetrias(self.machine_id, telemetrias)
                        
                        # Remover telemetrias enviadas com sucesso
                        for id_telemetria in ids_enviadas:
                            self.fila.remover_telemetria(id_telemetria)
                        
                        self.logger.info(f'{len(telemetrias)} telemetrias enviadas com sucesso')
                        
                    except Exception as e:
                        self.logger.error(f'Erro ao enviar telemetrias: {str(e)}')
                        # Incrementar tentativas
                        for id_telemetria in ids_enviadas:
                            self.fila.incrementar_tentativas(id_telemetria)
                
                # Limpar telemetrias antigas
                try:
                    removidas = self.fila.limpar_antigas()
                    if removidas > 0:
                        self.logger.debug(f'{removidas} telemetrias antigas removidas')
                except Exception as e:
                    self.logger.error(f'Erro ao limpar telemetrias antigas: {str(e)}')
                
            except Exception as e:
                self.logger.error(f'Erro no ciclo de envio: {str(e)}')
            
            # Aguardar próximo ciclo
            time.sleep(Configuracao.INTERVALO_ENVIO)
    
    def parar(self):
        """Para o serviço"""
        self.logger.info('Parando agente de monitoramento...')
        self.em_execucao = False


def main():
    """Função principal"""
    agente = ServicoAgente()
    agente.iniciar()


if __name__ == '__main__':
    main()
