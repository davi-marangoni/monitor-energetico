from django.contrib import admin
from django.urls import include, path

from configuracao import views_web

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("configuracao.urls_api")),
    path("web/login/", views_web.LoginSistemaView.as_view(), name="web_login"),
    path("web/logout/", views_web.logout_view, name="web_logout"),
    path("web/", views_web.dashboard_view, name="web_dashboard"),
    path("web/maquinas/<int:maquina_id>/", views_web.maquina_view, name="web_maquina"),
    path("web/maquinas/<int:maquina_id>/configuracao/", views_web.configuracao_energetica_view, name="web_configuracao"),
]
