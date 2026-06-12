from django.contrib.auth.models import User
from rest_framework import serializers


class CadastroUsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "senha"]

    def create(self, validated_data):
        senha = validated_data.pop("senha")
        usuario = User(**validated_data)
        usuario.set_password(senha)
        usuario.save()
        return usuario


class UsuarioAtualSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
