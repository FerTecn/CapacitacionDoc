# Generated by Django 5.1.4 on 2025-01-24 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0003_rename_fecha_evento_fechafin_evento_dias_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='dias',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
