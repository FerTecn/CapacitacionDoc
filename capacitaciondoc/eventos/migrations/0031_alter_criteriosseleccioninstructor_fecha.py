# Generated by Django 5.1.4 on 2025-03-29 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0030_alter_criteriosseleccioninstructor_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criteriosseleccioninstructor',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
    ]
