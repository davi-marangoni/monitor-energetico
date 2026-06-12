from decimal import Decimal


class ServicoCalculoEnergetico:
    @staticmethod
    def calcular_consumo_cpu(percentual_uso_cpu, tdp_cpu_watts, fator_idle_alpha):
        uso = Decimal(str(percentual_uso_cpu))
        tdp = Decimal(str(tdp_cpu_watts))
        alpha = Decimal(str(fator_idle_alpha))
        return tdp * (alpha + (Decimal("1") - alpha) * uso / Decimal("100"))

    @staticmethod
    def calcular_consumo_ram(ram_utilizada_gb, consumo_ram_por_gb):
        ram = Decimal(str(ram_utilizada_gb))
        consumo_gb = Decimal(str(consumo_ram_por_gb))
        return ram * consumo_gb

    @classmethod
    def calcular_consumo_total(cls, telemetria, configuracao):
        consumo_cpu = cls.calcular_consumo_cpu(
            telemetria.percentual_uso_cpu,
            configuracao.tdp_cpu_watts,
            configuracao.fator_idle_alpha,
        )
        consumo_ram = cls.calcular_consumo_ram(
            telemetria.ram_utilizada_gb,
            configuracao.consumo_ram_por_gb,
        )
        return float(consumo_cpu + consumo_ram)
