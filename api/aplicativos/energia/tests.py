from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import ConfiguracaoEnergetica
from .servicos.servico_calculo_energetico import ServicoCalculoEnergetico
from aplicativos.maquinas.models import Maquina
from aplicativos.telemetria.models import Telemetria
from django.utils import timezone


class ConfiguracaoEnergeticaTestCase(TestCase):
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
    
    def test_criar_configuracao_energetica(self):
        """Testa se uma configuração energética pode ser criada"""
        data = {
            'maquina': self.maquina.id,
            'tdp_cpu_watts': 95.0,
            'fator_idle_alpha': 0.3,
            'consumo_ram_por_gb': 0.5
        }
        response = self.client.post('/api/configuracoes-energeticas/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ConfiguracaoEnergetica.objects.filter(maquina=self.maquina).exists())
    
    def test_listar_configuracoes_energeticas(self):
        """Testa se as configurações energéticas são listadas"""
        ConfiguracaoEnergetica.objects.create(
            maquina=self.maquina,
            tdp_cpu_watts=95.0,
            fator_idle_alpha=0.3,
            consumo_ram_por_gb=0.5
        )
        
        response = self.client.get('/api/configuracoes-energeticas/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class ServicoCalculoEnergeticoTestCase(TestCase):
    def test_calculo_consumo_cpu(self):
        """Testa o cálculo de consumo da CPU"""
        consumo = ServicoCalculoEnergetico.calcular_consumo_cpu(
            tdp_watts=95.0,
            fator_idle=0.3,
            percentual_uso=50.0
        )
        esperado = 95.0 * (0.3 + (1 - 0.3) * (50.0 / 100))
        self.assertAlmostEqual(consumo, round(esperado, 2), places=2)
    
    def test_calculo_consumo_ram(self):
        """Testa o cálculo de consumo da RAM"""
        consumo = ServicoCalculoEnergetico.calcular_consumo_ram(
            ram_utilizada_gb=8.0,
            consumo_por_gb=0.5
        )
        self.assertEqual(consumo, 4.0)
    
    def test_calculo_consumo_total(self):
        """Testa o cálculo do consumo total"""
        consumo = ServicoCalculoEnergetico.calcular_consumo_total(
            consumo_cpu=50.0,
            consumo_ram=4.0
        )
        self.assertEqual(consumo, 54.0)
    
    def test_calculo_consumo_completo(self):
        """Testa o cálculo completo de consumo"""
        maquina = Maquina.objects.create(
            usuario=User.objects.create_user(username='testuser'),
            hostname='teste',
            machine_id_linux='123',
            modelo_cpu='Intel',
            total_ram_gb=16.0,
            nome_sistema_operacional='Linux',
            versao_sistema_operacional='5.15'
        )
        
        config = ConfiguracaoEnergetica.objects.create(
            maquina=maquina,
            tdp_cpu_watts=95.0,
            fator_idle_alpha=0.3,
            consumo_ram_por_gb=0.5
        )
        
        telemetria = Telemetria.objects.create(
            maquina=maquina,
            percentual_uso_cpu=50.0,
            ram_utilizada_gb=8.0,
            coletado_em=timezone.now()
        )
        
        consumo = ServicoCalculoEnergetico.calcular_consumo_completo(telemetria, config)
        
        self.assertIn('consumo_cpu', consumo)
        self.assertIn('consumo_ram', consumo)
        self.assertIn('consumo_total', consumo)
        self.assertEqual(consumo['consumo_ram'], 4.0)
