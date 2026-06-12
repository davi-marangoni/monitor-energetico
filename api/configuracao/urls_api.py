from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from aplicativos.usuarios.views import AutenticacaoCadastroView, AutenticacaoMeView
from aplicativos.maquinas.views import MaquinaDetalheAtualizacaoView, MaquinaListarView, MaquinaRegistrarView
from aplicativos.telemetria.views import TelemetriaHistoricoView, TelemetriaListarView, TelemetriaLoteView
from aplicativos.energia.views import ConfiguracaoEnergeticaDetalheView, ConfiguracaoEnergeticaListarCriarView

urlpatterns = [
    path("autenticacao/cadastro", AutenticacaoCadastroView.as_view(), name="autenticacao_cadastro"),
    path("autenticacao/login", TokenObtainPairView.as_view(), name="autenticacao_login"),
    path("autenticacao/refresh", TokenRefreshView.as_view(), name="autenticacao_refresh"),
    path("autenticacao/me", AutenticacaoMeView.as_view(), name="autenticacao_me"),
    path("maquinas", MaquinaListarView.as_view(), name="maquinas_listar"),
    path("maquinas/registrar", MaquinaRegistrarView.as_view(), name="maquinas_registrar"),
    path("maquinas/<int:id>", MaquinaDetalheAtualizacaoView.as_view(), name="maquinas_detalhe"),
    path("telemetrias/lote", TelemetriaLoteView.as_view(), name="telemetrias_lote"),
    path("telemetrias", TelemetriaListarView.as_view(), name="telemetrias_listar"),
    path("telemetrias/historico", TelemetriaHistoricoView.as_view(), name="telemetrias_historico"),
    path("configuracoes-energeticas", ConfiguracaoEnergeticaListarCriarView.as_view(), name="configuracoes_energeticas"),
    path("configuracoes-energeticas/<int:id>", ConfiguracaoEnergeticaDetalheView.as_view(), name="configuracoes_energeticas_detalhe"),
]
