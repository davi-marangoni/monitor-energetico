from django.contrib import admin
from .models import ConfiguracaoEnergetica


@admin.register(ConfiguracaoEnergetica)
class ConfiguracaoEnergeticaAdmin(admin.ModelAdmin):
    list_display = ('maquina', 'tdp_cpu_watts', 'fator_idle_alpha', 'consumo_ram_por_gb', 'ativo', 'atualizado_em')
    list_filter = ('ativo', 'atualizado_em')
    search_fields = ('maquina__hostname', 'maquina__machine_id_linux')
    readonly_fields = ('criado_em', 'atualizado_em')
    fieldsets = (
        ('Máquina', {
            'fields': ('maquina', 'ativo')
        }),
        ('Configuração Energética', {
            'fields': ('tdp_cpu_watts', 'fator_idle_alpha', 'consumo_ram_por_gb')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em')
        }),
    )
