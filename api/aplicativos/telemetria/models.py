from django.db import models

from aplicativos.maquinas.models import Maquina


class Telemetria(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name="telemetrias")
    percentual_uso_cpu = models.DecimalField(max_digits=5, decimal_places=2)
    ram_utilizada_gb = models.DecimalField(max_digits=10, decimal_places=3)
    coletado_em = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "telemetrias"
        indexes = [models.Index(fields=["maquina", "coletado_em"])]

    def __str__(self):
        return f"Telemetria {self.maquina_id} em {self.coletado_em}"
