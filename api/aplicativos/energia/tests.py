from decimal import Decimal

from django.test import TestCase

from aplicativos.energia.servicos import ServicoCalculoEnergetico


class ServicoCalculoEnergeticoTestes(TestCase):
    def test_calculo_cpu(self):
        resultado = ServicoCalculoEnergetico.calcular_consumo_cpu(50, 100, Decimal("0.2"))
        self.assertEqual(resultado, Decimal("60.0"))

    def test_calculo_ram(self):
        resultado = ServicoCalculoEnergetico.calcular_consumo_ram(8, Decimal("0.5"))
        self.assertEqual(resultado, Decimal("4.0"))
