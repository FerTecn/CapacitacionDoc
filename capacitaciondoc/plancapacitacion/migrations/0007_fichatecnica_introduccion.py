# Generated by Django 5.1.4 on 2025-02-07 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plancapacitacion', '0006_alter_fichatecnica_justificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichatecnica',
            name='introduccion',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
