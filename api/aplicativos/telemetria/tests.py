from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from aplicativos.maquinas.models import Maquina


class TelemetriaLoteApiTestes(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="teste")
        self.client = APIClient()
        self.client.force_authenticate(self.usuario)
        self.maquina = Maquina.objects.create(
            usuario=self.usuario,
            hostname="pc",
            machine_id_linux="abc123",
            modelo_cpu="cpu",
            total_ram_gb=16,
            nome_sistema_operacional="Linux",
            versao_sistema_operacional="6.8",
        )

    def test_envio_lote(self):
        resposta = self.client.post(
            "/api/telemetrias/lote",
            {
                "machine_id": "abc123",
                "telemetrias": [
                    {
                        "percentual_uso_cpu": 35,
                        "ram_utilizada_gb": 8.2,
                        "coletado_em": (timezone.now() - timedelta(minutes=1)).isoformat(),
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.data["recebidas"], 1)
