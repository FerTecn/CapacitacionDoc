# Generated by Django 5.1.4 on 2024-12-16 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plancapacitacion', '0002_alter_registrocurso_horas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrocurso',
            name='horas',
            field=models.IntegerField(),
        ),
    ]
