import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('maquinas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Telemetria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentual_uso_cpu', models.FloatField()),
                ('ram_utilizada_gb', models.FloatField()),
                ('coletado_em', models.DateTimeField()),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telemetrias', to='maquinas.maquina')),
            ],
            options={
                'verbose_name': 'Telemetria',
                'verbose_name_plural': 'Telemetrias',
                'ordering': ['-coletado_em'],
            },
        ),
        migrations.AddIndex(
            model_name='telemetria',
            index=models.Index(fields=['maquina', 'coletado_em'], name='aplicativos__maquina_4c8e2b_idx'),
        ),
        migrations.AddIndex(
            model_name='telemetria',
            index=models.Index(fields=['coletado_em'], name='aplicativos__coletad_91a3f7_idx'),
        ),
    ]
