# Generated by Django 5.1.4 on 2025-02-08 03:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0013_alter_instructor_fechanac'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docente',
            name='departamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.departamento', verbose_name='Departamento'),
        ),
        migrations.AlterField(
            model_name='docente',
            name='fechaNac',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='docente',
            name='genero',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.genero', verbose_name='Género'),
        ),
        migrations.AlterField(
            model_name='experiencialaboral',
            name='fecha_fin',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='experiencialaboral',
            name='fecha_inicio',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='formacionacademica',
            name='grado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.gradoacademico', verbose_name='Grado Académico'),
        ),
        migrations.AlterField(
            model_name='participacioninstructor',
            name='periodoFin',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='participacioninstructor',
            name='periodoInicio',
            field=models.DateField(null=True),
        ),
    ]
