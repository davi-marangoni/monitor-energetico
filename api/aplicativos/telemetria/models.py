from django.db import models
from aplicativos.maquinas.models import Maquina


class Telemetria(models.Model):
    """
    Modelo que representa uma coleta de dados realizada pelo agente.
    Armazena apenas dados brutos coletados pelo agente.
    """
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='telemetrias')
    percentual_uso_cpu = models.FloatField()
    ram_utilizada_gb = models.FloatField()
    coletado_em = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Telemetria'
        verbose_name_plural = 'Telemetrias'
        ordering = ['-coletado_em']
        indexes = [
            models.Index(fields=['maquina', 'coletado_em']),
            models.Index(fields=['coletado_em']),
        ]

    def __str__(self):
        return f'Telemetria {self.maquina} em {self.coletado_em}'
