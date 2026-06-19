from aplicativos.energia.models import ConfiguracaoEnergetica
from aplicativos.energia.servicos.servico_dashboard import (
    calcular_consumo_telemetria,
    montar_dados_maquina,
    obter_configuracao_ou_defaults,
    obter_ranking_maquinas,
    obter_resumo_dashboard,
    obter_ultima_telemetria,
)
from aplicativos.maquinas.models import Maquina
from aplicativos.maquinas.utils import maquina_esta_online


def obter_maquina_do_usuario(usuario, maquina_id):
    return Maquina.objects.get(id=maquina_id, usuario=usuario)


def montar_contexto_dashboard(usuario):
    resumo = obter_resumo_dashboard(usuario)
    _, ranking = obter_ranking_maquinas(usuario, limite=100)
    return {
        **resumo,
        'ranking': ranking,
    }


def montar_contexto_maquina(maquina):
    telemetria = obter_ultima_telemetria(maquina)
    configuracao = obter_configuracao_ou_defaults(maquina)
    current_state = {
        'cpu': 0,
        'ram': 0,
        'consumption': 0,
    }

    if telemetria:
        current_state['cpu'] = round(telemetria.percentual_uso_cpu, 1)
        ram_percent = (telemetria.ram_utilizada_gb / maquina.total_ram_gb * 100) if maquina.total_ram_gb else 0
        current_state['ram'] = round(ram_percent, 1)
        consumo = calcular_consumo_telemetria(telemetria, configuracao)
        current_state['consumption'] = consumo['consumo_total']

    maquina.online = maquina_esta_online(maquina)

    return {
        'machine': maquina,
        'current_state': current_state,
    }


def obter_ou_criar_configuracao(maquina):
    configuracao, _ = ConfiguracaoEnergetica.objects.get_or_create(
        maquina=maquina,
        defaults={
            'tdp_cpu_watts': 65.0,
            'fator_idle_alpha': 0.3,
            'consumo_ram_por_gb': 0.5,
            'ativo': True,
        },
    )
    return configuracao


def listar_maquinas_com_status(usuario):
    maquinas = Maquina.objects.filter(usuario=usuario).order_by('-atualizado_em')
    return [montar_dados_maquina(maquina) for maquina in maquinas]
