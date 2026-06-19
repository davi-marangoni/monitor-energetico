import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('maquinas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoEnergetica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tdp_cpu_watts', models.FloatField(help_text='Potência TDP da CPU em watts')),
                ('fator_idle_alpha', models.FloatField(default=0.3, help_text='Fator de inatividade (0 a 1)')),
                ('consumo_ram_por_gb', models.FloatField(help_text='Consumo de energia por GB de RAM em watts')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('maquina', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='configuracao_energetica', to='maquinas.maquina')),
            ],
            options={
                'verbose_name': 'Configuração Energética',
                'verbose_name_plural': 'Configurações Energéticas',
                'ordering': ['-atualizado_em'],
            },
        ),
    ]
