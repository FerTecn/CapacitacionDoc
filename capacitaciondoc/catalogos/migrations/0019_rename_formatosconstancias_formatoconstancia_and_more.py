# Generated by Django 5.1.4 on 2025-02-21 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0018_formatosconstancias_formatosdepartamento'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FormatosConstancias',
            new_name='FormatoConstancia',
        ),
        migrations.RenameModel(
            old_name='FormatosDepartamento',
            new_name='FormatoDepartamento',
        ),
    ]
