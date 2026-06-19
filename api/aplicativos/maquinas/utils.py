from datetime import timedelta

from django.utils import timezone


def maquina_esta_online(maquina, threshold_minutos=5):
    if not maquina.ultimo_ping_em:
        return False
    limite = timezone.now() - timedelta(minutes=threshold_minutos)
    return maquina.ultimo_ping_em >= limite
