# Generated by Django 5.1.4 on 2025-01-21 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0004_remove_instructor_cedulaprof_remove_instructor_curso_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiencialaboral',
            name='fecha_fin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experiencialaboral',
            name='fecha_inicio',
            field=models.DateField(blank=True, null=True),
        ),
    ]
