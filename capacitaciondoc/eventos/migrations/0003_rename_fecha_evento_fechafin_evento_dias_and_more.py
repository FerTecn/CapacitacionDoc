# Generated by Django 5.1.4 on 2025-01-24 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0002_horario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evento',
            old_name='fecha',
            new_name='fechaFin',
        ),
        migrations.AddField(
            model_name='evento',
            name='dias',
            field=models.TextField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evento',
            name='fechaInicio',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='horaFin',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='horaInicio',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Horario',
        ),
    ]
