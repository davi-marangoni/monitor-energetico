from django.contrib import admin
from .models import Maquina


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'machine_id_linux', 'usuario', 'ativo', 'ultimo_ping_em', 'atualizado_em')
    list_filter = ('ativo', 'usuario', 'atualizado_em')
    search_fields = ('hostname', 'machine_id_linux')
    readonly_fields = ('machine_id_linux', 'criado_em', 'atualizado_em')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'hostname', 'machine_id_linux', 'ativo')
        }),
        ('Hardware', {
            'fields': ('modelo_cpu', 'total_ram_gb', 'nome_sistema_operacional', 'versao_sistema_operacional')
        }),
        ('Configuração', {
            'fields': ('intervalo_coleta_segundos', 'intervalo_envio_segundos')
        }),
        ('Datas', {
            'fields': ('ultimo_ping_em', 'criado_em', 'atualizado_em')
        }),
    )
