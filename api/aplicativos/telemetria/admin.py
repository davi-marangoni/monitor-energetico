from django.contrib import admin
from .models import Telemetria


@admin.register(Telemetria)
class TelemetriaAdmin(admin.ModelAdmin):
    list_display = ('maquina', 'percentual_uso_cpu', 'ram_utilizada_gb', 'coletado_em', 'criado_em')
    list_filter = ('maquina', 'coletado_em', 'criado_em')
    search_fields = ('maquina__hostname', 'maquina__machine_id_linux')
    readonly_fields = ('criado_em',)
    fieldsets = (
        ('Informações', {
            'fields': ('maquina', 'percentual_uso_cpu', 'ram_utilizada_gb')
        }),
        ('Datas', {
            'fields': ('coletado_em', 'criado_em')
        }),
    )
    date_hierarchy = 'coletado_em'
