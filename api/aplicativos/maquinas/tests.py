from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Maquina
from datetime import datetime


class MaquinaTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='senhaSegura123')
        
        # Login e obter token
        login_data = {'username': 'testuser', 'password': 'senhaSegura123'}
        login_response = self.client.post('/api/autenticacao/login', login_data, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'******')
    
    def test_registrar_maquina(self):
        """Testa se uma máquina pode ser registrada"""
        data = {
            'hostname': 'maquina-teste',
            'machine_id_linux': 'abc123def456',
            'modelo_cpu': 'Intel Core i7',
            'total_ram_gb': 16.0,
            'nome_sistema_operacional': 'Linux',
            'versao_sistema_operacional': '5.15.0',
            'intervalo_coleta_segundos': 60,
            'intervalo_envio_segundos': 300,
        }
        response = self.client.post('/api/maquinas/registrar', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Maquina.objects.filter(machine_id_linux='abc123def456').exists())
    
    def test_listar_maquinas(self):
        """Testa se as máquinas do usuário são listadas"""
        Maquina.objects.create(
            usuario=self.user,
            hostname='maquina-teste',
            machine_id_linux='abc123def456',
            modelo_cpu='Intel Core i7',
            total_ram_gb=16.0,
            nome_sistema_operacional='Linux',
            versao_sistema_operacional='5.15.0'
        )
        
        response = self.client.get('/api/maquinas/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_atualizar_maquina(self):
        """Testa se uma máquina pode ser atualizada"""
        maquina = Maquina.objects.create(
            usuario=self.user,
            hostname='maquina-teste',
            machine_id_linux='abc123def456',
            modelo_cpu='Intel Core i7',
            total_ram_gb=16.0,
            nome_sistema_operacional='Linux',
            versao_sistema_operacional='5.15.0'
        )
        
        data = {
            'intervalo_coleta_segundos': 120,
            'ativo': False
        }
        response = self.client.patch(f'/api/maquinas/{maquina.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        maquina.refresh_from_db()
        self.assertEqual(maquina.intervalo_coleta_segundos, 120)
        self.assertFalse(maquina.ativo)
