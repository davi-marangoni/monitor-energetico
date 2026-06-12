from datetime import timedelta

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from aplicativos.energia.models import ConfiguracaoEnergetica
from aplicativos.energia.servicos import ServicoCalculoEnergetico
from aplicativos.maquinas.models import Maquina
from aplicativos.telemetria.models import Telemetria


class LoginSistemaView(LoginView):
    template_name = "sistema_web/login.html"


def logout_view(request):
    logout(request)
    return redirect("web_login")


@login_required
def dashboard_view(request):
    agora = timezone.now()
    limite_online = agora - timedelta(minutes=5)
    maquinas = Maquina.objects.filter(usuario=request.user, ativo=True)
    online = maquinas.filter(ultimo_ping_em__gte=limite_online).count()
    offline = max(maquinas.count() - online, 0)

    consumo_total_atual = 0.0
    consumos = []
    for maquina in maquinas:
        telemetria = Telemetria.objects.filter(maquina=maquina).order_by("-coletado_em").first()
        config = ConfiguracaoEnergetica.objects.filter(maquina=maquina, ativo=True).order_by("-atualizado_em").first()
        if telemetria and config:
            consumo = ServicoCalculoEnergetico.calcular_consumo_total(telemetria, config)
            consumo_total_atual += consumo
            consumos.append((maquina, consumo))

    consumo_medio = consumo_total_atual / len(consumos) if consumos else 0.0
    ranking = sorted(consumos, key=lambda item: item[1], reverse=True)[:5]

    return render(
        request,
        "sistema_web/dashboard.html",
        {
            "online": online,
            "offline": offline,
            "consumo_total_atual": round(consumo_total_atual, 2),
            "consumo_medio": round(consumo_medio, 2),
            "ranking": ranking,
            "maquinas": maquinas,
        },
    )


@login_required
def maquina_view(request, maquina_id):
    maquina = get_object_or_404(Maquina, id=maquina_id, usuario=request.user)
    telemetrias = Telemetria.objects.filter(maquina=maquina).order_by("-coletado_em")[:100]
    telemetrias = list(reversed(telemetrias))
    config = ConfiguracaoEnergetica.objects.filter(maquina=maquina, ativo=True).order_by("-atualizado_em").first()
    consumos = [round(ServicoCalculoEnergetico.calcular_consumo_total(t, config), 4) if config else 0 for t in telemetrias]

    return render(
        request,
        "sistema_web/maquina.html",
        {
            "maquina": maquina,
            "telemetrias": telemetrias,
            "consumos": consumos,
            "config": config,
        },
    )


@login_required
def configuracao_energetica_view(request, maquina_id):
    maquina = get_object_or_404(Maquina, id=maquina_id, usuario=request.user)
    atual = ConfiguracaoEnergetica.objects.filter(maquina=maquina, ativo=True).order_by("-atualizado_em").first()

    if request.method == "POST":
        if atual:
            atual.ativo = False
            atual.save(update_fields=["ativo", "atualizado_em"])
        ConfiguracaoEnergetica.objects.create(
            maquina=maquina,
            tdp_cpu_watts=request.POST.get("tdp_cpu_watts", 65),
            fator_idle_alpha=request.POST.get("fator_idle_alpha", 0.2),
            consumo_ram_por_gb=request.POST.get("consumo_ram_por_gb", 0.3),
            ativo=True,
        )
        return redirect("web_configuracao", maquina_id=maquina.id)

    return render(request, "sistema_web/configuracao.html", {"maquina": maquina, "atual": atual})
