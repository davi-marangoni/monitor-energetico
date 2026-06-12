import requests


class ClienteApiMonitor:
    def __init__(self, api_url, usuario, senha, timeout=15):
        self.api_url = api_url.rstrip("/")
        self.usuario = usuario
        self.senha = senha
        self.timeout = timeout
        self._access_token = None

    def autenticar(self):
        resposta = requests.post(
            f"{self.api_url}/autenticacao/login",
            json={"username": self.usuario, "password": self.senha},
            timeout=self.timeout,
        )
        resposta.raise_for_status()
        self._access_token = resposta.json()["access"]

    @property
    def _headers(self):
        if not self._access_token:
            self.autenticar()
        return {"Authorization": "Bearer " + self._access_token}

    def registrar_maquina(self, dados_maquina):
        resposta = requests.post(
            f"{self.api_url}/maquinas/registrar",
            json=dados_maquina,
            headers=self._headers,
            timeout=self.timeout,
        )
        resposta.raise_for_status()
        return resposta.json()

    def enviar_lote_telemetria(self, machine_id_linux, telemetrias):
        resposta = requests.post(
            f"{self.api_url}/telemetrias/lote",
            json={"machine_id": machine_id_linux, "telemetrias": telemetrias},
            headers=self._headers,
            timeout=self.timeout,
        )
        if resposta.status_code == 401:
            self.autenticar()
            return self.enviar_lote_telemetria(machine_id_linux, telemetrias)
        resposta.raise_for_status()
        return resposta.json()
