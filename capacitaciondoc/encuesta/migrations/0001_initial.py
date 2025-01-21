# Generated by Django 5.1.4 on 2025-01-21 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instructor1', models.IntegerField()),
                ('instructor2', models.IntegerField()),
                ('instructor3', models.IntegerField()),
                ('instructor4', models.IntegerField()),
                ('instructor5', models.IntegerField()),
                ('instructor6', models.IntegerField()),
                ('instructor7', models.IntegerField()),
                ('curso1', models.IntegerField()),
                ('curso2', models.IntegerField()),
                ('curso3', models.IntegerField()),
                ('curso4', models.IntegerField()),
                ('material1', models.IntegerField()),
                ('material2', models.IntegerField()),
                ('material3', models.IntegerField()),
                ('insfraestructura1', models.IntegerField()),
                ('insfraestructura2', models.IntegerField()),
                ('insfraestructura3', models.IntegerField()),
                ('insfraestructura4', models.IntegerField()),
                ('insfraestructura5', models.IntegerField(blank=True, null=True)),
                ('insfraestructura6', models.IntegerField(blank=True, null=True)),
                ('comentarios', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
