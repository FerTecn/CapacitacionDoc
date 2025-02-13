# Generated by Django 5.1.4 on 2025-02-13 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0017_valorcalificacion_delete_calificacionvalor'),
        ('eventos', '0018_remove_calificacion_comentario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calificacion',
            name='calificacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.valorcalificacion'),
        ),
        migrations.AlterField(
            model_name='calificacion',
            name='inscripcion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eventos.inscripcion'),
        ),
    ]
