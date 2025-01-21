# Generated by Django 5.1.4 on 2025-01-21 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0005_experiencialaboral_fecha_fin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='participacioninstructor',
            name='periodoFin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='participacioninstructor',
            name='periodoInicio',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='participacioninstructor',
            name='fechaParticipacion',
            field=models.DateField(blank=True, null=True),
        ),
    ]
