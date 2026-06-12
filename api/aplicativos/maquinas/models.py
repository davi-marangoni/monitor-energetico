from django.conf import settings
from django.db import models


class Maquina(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="maquinas")
    hostname = models.CharField(max_length=255)
    machine_id_linux = models.CharField(max_length=255, unique=True)
    modelo_cpu = models.CharField(max_length=255, blank=True)
    total_ram_gb = models.DecimalField(max_digits=10, decimal_places=2)
    nome_sistema_operacional = models.CharField(max_length=128)
    versao_sistema_operacional = models.CharField(max_length=128)
    intervalo_coleta_segundos = models.PositiveIntegerField(default=10)
    intervalo_envio_segundos = models.PositiveIntegerField(default=60)
    ativo = models.BooleanField(default=True)
    ultimo_ping_em = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "maquinas"

    def __str__(self):
        return f"{self.hostname} ({self.machine_id_linux})"
