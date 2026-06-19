from datetime import timedelta

from django.utils import timezone

from aplicativos.energia.models import ConfiguracaoEnergetica
from aplicativos.energia.servicos.servico_calculo_energetico import ServicoCalculoEnergetico
from aplicativos.maquinas.models import Maquina
from aplicativos.maquinas.utils import maquina_esta_online
from aplicativos.telemetria.models import Telemetria

DEFAULT_TDP = 65.0
DEFAULT_FATOR_IDLE = 0.3
DEFAULT_CONSUMO_RAM_POR_GB = 0.5
ONLINE_THRESHOLD_MINUTES = 5


def obter_configuracao_ou_defaults(maquina):
    try:
        return maquina.configuracao_energetica
    except ConfiguracaoEnergetica.DoesNotExist:
        return None


def calcular_consumo_telemetria(telemetria, configuracao=None):
    if configuracao is None:
        consumo_cpu = ServicoCalculoEnergetico.calcular_consumo_cpu(
            DEFAULT_TDP, DEFAULT_FATOR_IDLE, telemetria.percentual_uso_cpu
        )
        consumo_ram = ServicoCalculoEnergetico.calcular_consumo_ram(
            telemetria.ram_utilizada_gb, DEFAULT_CONSUMO_RAM_POR_GB
        )
    else:
        resultado = ServicoCalculoEnergetico.calcular_consumo_completo(telemetria, configuracao)
        return resultado

    return {
        'consumo_cpu': consumo_cpu,
        'consumo_ram': consumo_ram,
        'consumo_total': ServicoCalculoEnergetico.calcular_consumo_total(consumo_cpu, consumo_ram),
    }


def obter_maquinas_usuario(usuario):
    return Maquina.objects.filter(usuario=usuario).select_related('configuracao_energetica')


def obter_ultima_telemetria(maquina):
    return maquina.telemetrias.order_by('-coletado_em').first()


def montar_dados_maquina(maquina):
    telemetria = obter_ultima_telemetria(maquina)
    configuracao = obter_configuracao_ou_defaults(maquina)
    consumo_total = None
    cpu_usage = None
    ram_usage = None

    if telemetria:
        cpu_usage = telemetria.percentual_uso_cpu
        ram_usage = telemetria.ram_utilizada_gb
        consumo = calcular_consumo_telemetria(telemetria, configuracao)
        consumo_total = consumo['consumo_total']

    return {
        'id': maquina.id,
        'hostname': maquina.hostname,
        'machine_id_linux': maquina.machine_id_linux,
        'cpu_usage': cpu_usage,
        'ram_usage': ram_usage,
        'consumption': consumo_total,
        'online': maquina_esta_online(maquina, ONLINE_THRESHOLD_MINUTES),
    }


def obter_resumo_dashboard(usuario):
    maquinas = list(obter_maquinas_usuario(usuario))
    online = 0
    offline = 0
    consumos = []

    for maquina in maquinas:
        if maquina_esta_online(maquina, ONLINE_THRESHOLD_MINUTES):
            online += 1
        else:
            offline += 1

        telemetria = obter_ultima_telemetria(maquina)
        if telemetria:
            configuracao = obter_configuracao_ou_defaults(maquina)
            consumo = calcular_consumo_telemetria(telemetria, configuracao)
            consumos.append(consumo['consumo_total'])

    current_consumption = sum(consumos) if consumos else 0
    average_consumption = round(sum(consumos) / len(consumos), 2) if consumos else 0

    return {
        'machines_online': online,
        'machines_offline': offline,
        'current_consumption': round(current_consumption, 2),
        'average_consumption': average_consumption,
    }


def obter_ranking_maquinas(usuario, limite=5):
    dados = [montar_dados_maquina(maquina) for maquina in obter_maquinas_usuario(usuario)]
    dados.sort(key=lambda item: item['consumption'] or 0, reverse=True)
    return dados[:limite], dados


def obter_consumo_geral(usuario, filtro='ultimas_24_horas'):
    agora = timezone.now()
    if filtro == 'ultima_hora':
        data_inicio = agora - timedelta(hours=1)
    elif filtro == 'ultimos_7_dias':
        data_inicio = agora - timedelta(days=7)
    elif filtro == 'ultimos_30_dias':
        data_inicio = agora - timedelta(days=30)
    else:
        data_inicio = agora - timedelta(hours=24)

    telemetrias = Telemetria.objects.filter(
        maquina__usuario=usuario,
        coletado_em__gte=data_inicio,
    ).select_related('maquina', 'maquina__configuracao_energetica').order_by('coletado_em')

    pontos = {}
    for telemetria in telemetrias:
        chave = telemetria.coletado_em.strftime('%H:%M')
        configuracao = obter_configuracao_ou_defaults(telemetria.maquina)
        consumo = calcular_consumo_telemetria(telemetria, configuracao)
        pontos[chave] = pontos.get(chave, 0) + consumo['consumo_total']

    labels = list(pontos.keys())
    valores = [round(valor, 2) for valor in pontos.values()]

    return {'labels': labels, 'values': valores}


def serializar_telemetria_com_consumo(telemetria):
    configuracao = obter_configuracao_ou_defaults(telemetria.maquina)
    consumo = calcular_consumo_telemetria(telemetria, configuracao)
    return {
        'id': telemetria.id,
        'maquina': telemetria.maquina_id,
        'percentual_uso_cpu': telemetria.percentual_uso_cpu,
        'ram_utilizada_gb': telemetria.ram_utilizada_gb,
        'coletado_em': telemetria.coletado_em,
        'criado_em': telemetria.criado_em,
        **consumo,
    }
