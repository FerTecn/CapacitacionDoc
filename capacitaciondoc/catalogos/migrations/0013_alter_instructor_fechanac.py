# Generated by Django 5.1.4 on 2025-02-08 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0012_alter_director_estatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='fechaNac',
            field=models.DateField(null=True),
        ),
    ]
