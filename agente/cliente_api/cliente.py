"""
Módulo cliente para comunicação com a API.
"""
import requests
import json
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ClienteAPI:
    """Cliente para comunicação com a API de monitoramento"""
    
    def __init__(self, url_base, username=None, ****** token=None):
        """Inicializa o cliente da API"""
        self.url_base = url_base.rstrip('/')
        self.username = username
        self.password = password
        self.token = token
        self.logger = logging.getLogger(__name__)
        
        # Configurar sessão com retry
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # Autenticar se necessário
        if username and password:
            self._autenticar_com_credenciais()
    
    def _autenticar_com_credenciais(self):
        """Realiza autenticação com username e password"""
        try:
            response = self.session.post(
                f'{self.url_base}/autenticacao/login',
                json={'username': self.username, 'password': self.password},
                timeout=10
            )
            response.raise_for_status()
            self.token = response.json()['access']
            self.logger.info('Autenticação realizada com sucesso')
        except Exception as e:
            self.logger.error(f'Erro ao autenticar: {str(e)}')
            raise
    
    def _obter_headers(self):
        """Retorna os headers para requisições"""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'******'
        return headers
    
    def registrar_maquina(self, dados_maquina):
        """Registra ou atualiza uma máquina na API"""
        try:
            response = self.session.post(
                f'{self.url_base}/maquinas/registrar',
                json=dados_maquina,
                headers=self._obter_headers(),
                timeout=10
            )
            response.raise_for_status()
            self.logger.info('Máquina registrada com sucesso')
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Erro ao registrar máquina: {str(e)}')
            raise
    
    def enviar_lote_telemetrias(self, machine_id, telemetrias):
        """Envia um lote de telemetrias para a API"""
        try:
            payload = {
                'machine_id': machine_id,
                'telemetrias': telemetrias
            }
            
            response = self.session.post(
                f'{self.url_base}/telemetrias/lote',
                json=payload,
                headers=self._obter_headers(),
                timeout=10
            )
            response.raise_for_status()
            self.logger.info(f'Lote de {len(telemetrias)} telemetrias enviado com sucesso')
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Erro ao enviar telemetrias: {str(e)}')
            raise
    
    def obter_configuracao_maquina(self, machine_id):
        """Obtém a configuração da máquina da API"""
        try:
            response = self.session.get(
                f'{self.url_base}/maquinas',
                headers=self._obter_headers(),
                params={'machine_id_linux': machine_id},
                timeout=10
            )
            response.raise_for_status()
            maquinas = response.json()
            if maquinas:
                return maquinas[0] if isinstance(maquinas, list) else maquinas
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Erro ao obter configuração: {str(e)}')
            raise
    
    def testar_conexao(self):
        """Testa a conexão com a API"""
        try:
            response = self.session.get(
                f'{self.url_base}/autenticacao/me',
                headers=self._obter_headers(),
                timeout=5
            )
            response.raise_for_status()
            self.logger.info('Conexão com API testada com sucesso')
            return True
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Erro ao testar conexão: {str(e)}')
            return False
