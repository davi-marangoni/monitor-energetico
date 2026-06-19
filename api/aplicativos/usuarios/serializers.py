from rest_framework import serializers
from django.contrib.auth.models import User


class UsuarioCadastroSerializer(serializers.ModelSerializer):
    """Serializer para cadastro de novo usuário"""
    senha = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'senha']
    
    def create(self, validated_data):
        senha = validated_data.pop('senha')
        usuario = User.objects.create_user(
            password=senha,
            **validated_data
        )
        return usuario


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para exibição de dados do usuário"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
