from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from .models import Telemetria
from aplicativos.maquinas.models import Maquina


class TelemetriaTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='senhaSegura123')
        
        # Login e obter token
        login_data = {'username': 'testuser', 'password': 'senhaSegura123'}
        login_response = self.client.post('/api/autenticacao/login', login_data, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Criar máquina
        self.maquina = Maquina.objects.create(
            usuario=self.user,
            hostname='maquina-teste',
            machine_id_linux='abc123def456',
            modelo_cpu='Intel Core i7',
            total_ram_gb=16.0,
            nome_sistema_operacional='Linux',
            versao_sistema_operacional='5.15.0'
        )
    
    def test_enviar_lote_telemetrias(self):
        """Testa se um lote de telemetrias pode ser enviado"""
        data = {
            'machine_id': 'abc123def456',
            'telemetrias': [
                {
                    'percentual_uso_cpu': '35.5',
                    'ram_utilizada_gb': '8.2',
                    'coletado_em': timezone.now().isoformat()
                },
                {
                    'percentual_uso_cpu': '45.0',
                    'ram_utilizada_gb': '9.1',
                    'coletado_em': timezone.now().isoformat()
                }
            ]
        }
        response = self.client.post('/api/telemetrias/lote/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Telemetria.objects.filter(maquina=self.maquina).count(), 2)
    
    def test_listar_telemetrias(self):
        """Testa se as telemetrias são listadas"""
        Telemetria.objects.create(
            maquina=self.maquina,
            percentual_uso_cpu=35.5,
            ram_utilizada_gb=8.2,
            coletado_em=timezone.now()
        )
        
        response = self.client.get('/api/telemetrias/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_historico_telemetrias(self):
        """Testa se o histórico de telemetrias pode ser filtrado"""
        Telemetria.objects.create(
            maquina=self.maquina,
            percentual_uso_cpu=35.5,
            ram_utilizada_gb=8.2,
            coletado_em=timezone.now()
        )
        
        response = self.client.get('/api/telemetrias/historico/?filtro=ultimas_24_horas', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
