import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=255)),
                ('machine_id_linux', models.CharField(max_length=255, unique=True)),
                ('modelo_cpu', models.CharField(max_length=255)),
                ('total_ram_gb', models.FloatField()),
                ('nome_sistema_operacional', models.CharField(max_length=255)),
                ('versao_sistema_operacional', models.CharField(max_length=255)),
                ('intervalo_coleta_segundos', models.IntegerField(default=60)),
                ('intervalo_envio_segundos', models.IntegerField(default=300)),
                ('ativo', models.BooleanField(default=True)),
                ('ultimo_ping_em', models.DateTimeField(blank=True, null=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maquinas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Máquina',
                'verbose_name_plural': 'Máquinas',
                'ordering': ['-atualizado_em'],
            },
        ),
        migrations.AddIndex(
            model_name='maquina',
            index=models.Index(fields=['usuario', 'ativo'], name='aplicativos__usuario_8a1f0d_idx'),
        ),
        migrations.AddIndex(
            model_name='maquina',
            index=models.Index(fields=['machine_id_linux'], name='aplicativos__machine__f8b2a1_idx'),
        ),
    ]
