# Generated by Django 5.1.4 on 2024-12-19 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0004_remove_evento_instructor_evento_fecha_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inscripcion',
            options={},
        ),
        migrations.AlterModelOptions(
            name='oficiocomision',
            options={'verbose_name_plural': 'Inscripciones'},
        ),
        migrations.RemoveField(
            model_name='inscripcion',
            name='clave',
        ),
        migrations.RemoveField(
            model_name='inscripcion',
            name='horas',
        ),
        migrations.RemoveField(
            model_name='inscripcion',
            name='instructor',
        ),
        migrations.RemoveField(
            model_name='inscripcion',
            name='nombre',
        ),
        migrations.AddField(
            model_name='inscripcion',
            name='evento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='eventos.evento'),
        ),
    ]
