# Generated by Django 5.1.4 on 2025-03-29 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plancapacitacion', '0011_concentradodiagnostico_actividadmodulosespecialidad_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actividadmodulosespecialidad',
            old_name='fecha',
            new_name='fechaRealizacion',
        ),
        migrations.RenameField(
            model_name='asignaturadeteccionnecesidades',
            old_name='noProfedores',
            new_name='noProfesores',
        ),
    ]
