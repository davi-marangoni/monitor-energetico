"""
Serviço responsável pelos cálculos de consumo energético.

As fórmulas implementadas são:
- Consumo_CPU = TDP × (α + (1 − α) × Uso_CPU / 100)
- Consumo_RAM = RAM_Utilizada × Consumo_Por_GB
- Consumo_Total = Consumo_CPU + Consumo_RAM
"""


class ServicoCalculoEnergetico:
    """
    Serviço para cálculos de consumo energético.
    Todos os cálculos são feitos dinamicamente sem persistência.
    """
    
    @staticmethod
    def calcular_consumo_cpu(tdp_watts, fator_idle, percentual_uso):
        """
        Calcula o consumo da CPU.
        
        Fórmula: Consumo_CPU = TDP × (α + (1 − α) × Uso_CPU / 100)
        
        Args:
            tdp_watts (float): Potência TDP da CPU em watts
            fator_idle (float): Fator de inatividade (0 a 1), típicamente 0.3
            percentual_uso (float): Percentual de utilização da CPU (0 a 100)
        
        Returns:
            float: Consumo da CPU em watts
        """
        if not (0 <= fator_idle <= 1):
            raise ValueError('fator_idle deve estar entre 0 e 1')
        if not (0 <= percentual_uso <= 100):
            raise ValueError('percentual_uso deve estar entre 0 e 100')
        
        consumo = tdp_watts * (fator_idle + (1 - fator_idle) * (percentual_uso / 100))
        return round(consumo, 2)
    
    @staticmethod
    def calcular_consumo_ram(ram_utilizada_gb, consumo_por_gb):
        """
        Calcula o consumo da RAM.
        
        Fórmula: Consumo_RAM = RAM_Utilizada × Consumo_Por_GB
        
        Args:
            ram_utilizada_gb (float): Quantidade de RAM utilizada em GB
            consumo_por_gb (float): Consumo de energia por GB de RAM em watts
        
        Returns:
            float: Consumo da RAM em watts
        """
        if ram_utilizada_gb < 0:
            raise ValueError('ram_utilizada_gb não pode ser negativo')
        if consumo_por_gb < 0:
            raise ValueError('consumo_por_gb não pode ser negativo')
        
        consumo = ram_utilizada_gb * consumo_por_gb
        return round(consumo, 2)
    
    @staticmethod
    def calcular_consumo_total(consumo_cpu, consumo_ram):
        """
        Calcula o consumo total de energia.
        
        Fórmula: Consumo_Total = Consumo_CPU + Consumo_RAM
        
        Args:
            consumo_cpu (float): Consumo da CPU em watts
            consumo_ram (float): Consumo da RAM em watts
        
        Returns:
            float: Consumo total em watts
        """
        return round(consumo_cpu + consumo_ram, 2)
    
    @staticmethod
    def calcular_consumo_completo(telemetria, configuracao_energetica):
        """
        Calcula o consumo completo para uma telemetria.
        
        Args:
            telemetria: Objeto de telemetria com percentual_uso_cpu e ram_utilizada_gb
            configuracao_energetica: Objeto de configuração energética
        
        Returns:
            dict: Dicionário com consumo_cpu, consumo_ram e consumo_total
        """
        consumo_cpu = ServicoCalculoEnergetico.calcular_consumo_cpu(
            tdp_watts=configuracao_energetica.tdp_cpu_watts,
            fator_idle=configuracao_energetica.fator_idle_alpha,
            percentual_uso=telemetria.percentual_uso_cpu
        )
        
        consumo_ram = ServicoCalculoEnergetico.calcular_consumo_ram(
            ram_utilizada_gb=telemetria.ram_utilizada_gb,
            consumo_por_gb=configuracao_energetica.consumo_ram_por_gb
        )
        
        consumo_total = ServicoCalculoEnergetico.calcular_consumo_total(
            consumo_cpu=consumo_cpu,
            consumo_ram=consumo_ram
        )
        
        return {
            'consumo_cpu': consumo_cpu,
            'consumo_ram': consumo_ram,
            'consumo_total': consumo_total,
        }
