from django.db import models
from django.contrib.auth.models import User


class Maquina(models.Model):
    """
    Modelo que representa uma máquina monitorada.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maquinas')
    hostname = models.CharField(max_length=255)
    machine_id_linux = models.CharField(max_length=255, unique=True)
    modelo_cpu = models.CharField(max_length=255)
    total_ram_gb = models.FloatField()
    nome_sistema_operacional = models.CharField(max_length=255)
    versao_sistema_operacional = models.CharField(max_length=255)
    intervalo_coleta_segundos = models.IntegerField(default=60)
    intervalo_envio_segundos = models.IntegerField(default=300)
    ativo = models.BooleanField(default=True)
    ultimo_ping_em = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Máquina'
        verbose_name_plural = 'Máquinas'
        ordering = ['-atualizado_em']
        indexes = [
            models.Index(fields=['usuario', 'ativo']),
            models.Index(fields=['machine_id_linux']),
        ]

    def __str__(self):
        return f'{self.hostname} ({self.machine_id_linux})'
