# Generated by Django 5.1.4 on 2025-01-23 02:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0008_alter_formacionacademica_grado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formacionacademica',
            name='grado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.gradoacademico', verbose_name='Grado Académico'),
        ),
    ]
