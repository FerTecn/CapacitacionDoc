# Generated by Django 5.1.4 on 2025-02-26 07:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0002_alter_encuesta_options_encuesta_curso_and_more'),
        ('eventos', '0023_oficiocomision_nomenclatura'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='encuesta',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='inscripcion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='encuestas', to='eventos.inscripcion'),
        ),
        migrations.RemoveField(
            model_name='encuesta',
            name='curso',
        ),
        migrations.RemoveField(
            model_name='encuesta',
            name='docente',
        ),
    ]
