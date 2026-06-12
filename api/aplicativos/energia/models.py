from django.db import models

from aplicativos.maquinas.models import Maquina


class ConfiguracaoEnergetica(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name="configuracoes_energeticas")
    tdp_cpu_watts = models.DecimalField(max_digits=10, decimal_places=2)
    fator_idle_alpha = models.DecimalField(max_digits=5, decimal_places=4)
    consumo_ram_por_gb = models.DecimalField(max_digits=10, decimal_places=4)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "configuracoes_energeticas"

    def __str__(self):
        return f"Configuração energética #{self.id} - {self.maquina.hostname}"
