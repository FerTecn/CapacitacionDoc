# Generated by Django 5.1.4 on 2025-01-24 00:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='eventos.evento')),
            ],
            options={
                'verbose_name_plural': 'Horarios',
            },
        ),
    ]
