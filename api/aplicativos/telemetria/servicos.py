from datetime import timedelta

from django.utils import timezone

from aplicativos.energia.models import ConfiguracaoEnergetica
from aplicativos.energia.servicos import ServicoCalculoEnergetico
from aplicativos.maquinas.models import Maquina
from aplicativos.telemetria.models import Telemetria


class ServicoTelemetria:
    @staticmethod
    def salvar_lote(usuario, machine_id, leituras):
        maquina = Maquina.objects.filter(machine_id_linux=machine_id, usuario=usuario).first()
        if not maquina:
            raise ValueError("Máquina não encontrada")
        objetos = [
            Telemetria(
                maquina=maquina,
                percentual_uso_cpu=item["percentual_uso_cpu"],
                ram_utilizada_gb=item["ram_utilizada_gb"],
                coletado_em=item["coletado_em"],
            )
            for item in leituras
        ]
        Telemetria.objects.bulk_create(objetos, batch_size=1000)
        maquina.ultimo_ping_em = timezone.now()
        maquina.save(update_fields=["ultimo_ping_em", "atualizado_em"])
        return len(objetos)

    @staticmethod
    def listar(usuario, maquina_id=None):
        filtro = {"maquina__usuario": usuario}
        if maquina_id:
            filtro["maquina_id"] = maquina_id
        return Telemetria.objects.filter(**filtro).order_by("-coletado_em")

    @staticmethod
    def historico_com_consumo(usuario, periodo=None, inicio=None, fim=None, maquina_id=None):
        telemetrias = ServicoTelemetria.listar(usuario, maquina_id)
        agora = timezone.now()
        if periodo == "ultima_hora":
            telemetrias = telemetrias.filter(coletado_em__gte=agora - timedelta(hours=1))
        elif periodo == "ultimas_24_horas":
            telemetrias = telemetrias.filter(coletado_em__gte=agora - timedelta(hours=24))
        elif periodo == "ultimos_7_dias":
            telemetrias = telemetrias.filter(coletado_em__gte=agora - timedelta(days=7))
        elif periodo == "ultimos_30_dias":
            telemetrias = telemetrias.filter(coletado_em__gte=agora - timedelta(days=30))

        if inicio:
            telemetrias = telemetrias.filter(coletado_em__gte=inicio)
        if fim:
            telemetrias = telemetrias.filter(coletado_em__lte=fim)

        resposta = []
        for telemetria in telemetrias.select_related("maquina"):
            config = ConfiguracaoEnergetica.objects.filter(maquina=telemetria.maquina, ativo=True).order_by("-atualizado_em").first()
            consumo = ServicoCalculoEnergetico.calcular_consumo_total(telemetria, config) if config else 0
            resposta.append(
                {
                    "maquina_id": telemetria.maquina_id,
                    "coletado_em": telemetria.coletado_em,
                    "percentual_uso_cpu": float(telemetria.percentual_uso_cpu),
                    "ram_utilizada_gb": float(telemetria.ram_utilizada_gb),
                    "consumo_estimado": round(consumo, 6),
                }
            )
        return resposta
