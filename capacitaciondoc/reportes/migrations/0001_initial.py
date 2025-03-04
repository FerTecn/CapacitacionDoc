# Generated by Django 5.1.4 on 2025-03-03 21:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eventos', '0027_alter_evidencia_archivo_evidencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConstanciaDocente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(null=True)),
                ('curso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eventos.calificacion')),
            ],
        ),
        migrations.CreateModel(
            name='ConstanciaInstructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(null=True)),
                ('curso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eventos.evento')),
            ],
        ),
    ]
