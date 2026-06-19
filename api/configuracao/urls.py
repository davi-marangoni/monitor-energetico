"""
URL configuration for the monitor_energetico project
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('aplicativos.interface_web.urls')),
    path('api/', include([
        path('autenticacao/', include('aplicativos.usuarios.urls')),
        path('maquinas/', include('aplicativos.maquinas.urls')),
        path('telemetrias/', include('aplicativos.telemetria.urls')),
        path('configuracoes-energeticas/', include('aplicativos.energia.urls')),
        path('dashboard/', include('aplicativos.energia.urls_dashboard')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
