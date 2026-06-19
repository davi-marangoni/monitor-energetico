from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class UsuarioCadastroTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_cadastro_usuario_sucesso(self):
        """Testa se um novo usuário pode ser cadastrado com sucesso"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'senha': 'senhaSegura123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post('/api/autenticacao/cadastro', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_login_usuario(self):
        """Testa se um usuário pode fazer login"""
        User.objects.create_user(username='testuser', password='senhaSegura123')
        
        data = {
            'username': 'testuser',
            'password': 'senhaSegura123'
        }
        response = self.client.post('/api/autenticacao/login', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_usuario_atual(self):
        """Testa se um usuário pode ver seus dados atuais"""
        user = User.objects.create_user(username='testuser', password='senhaSegura123')
        
        # Fazer login para obter token
        login_data = {
            'username': 'testuser',
            'password': 'senhaSegura123'
        }
        login_response = self.client.post('/api/autenticacao/login', login_data, format='json')
        token = login_response.data['access']
        
        # Usar token para acessar dados do usuário
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/autenticacao/me', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
