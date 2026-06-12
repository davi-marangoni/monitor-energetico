from django.db import models
from aplicativos.maquinas.models import Maquina


class ConfiguracaoEnergetica(models.Model):
    """
    Modelo que representa os parâmetros utilizados para cálculo energético.
    Todos os cálculos devem ocorrer dinamicamente na API.
    """
    maquina = models.OneToOneField(Maquina, on_delete=models.CASCADE, related_name='configuracao_energetica')
    tdp_cpu_watts = models.FloatField(help_text='Potência TDP da CPU em watts')
    fator_idle_alpha = models.FloatField(default=0.3, help_text='Fator de inatividade (0 a 1)')
    consumo_ram_por_gb = models.FloatField(help_text='Consumo de energia por GB de RAM em watts')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração Energética'
        verbose_name_plural = 'Configurações Energéticas'
        ordering = ['-atualizado_em']

    def __str__(self):
        return f'Configuração energética: {self.maquina}'
