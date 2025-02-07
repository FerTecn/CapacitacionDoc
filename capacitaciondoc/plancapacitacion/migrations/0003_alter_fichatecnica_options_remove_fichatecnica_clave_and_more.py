# Generated by Django 5.1.4 on 2025-02-06 23:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plancapacitacion', '0002_alter_registrocurso_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fichatecnica',
            options={'verbose_name_plural': 'Fichas técnicas'},
        ),
        migrations.RemoveField(
            model_name='fichatecnica',
            name='clave',
        ),
        migrations.RemoveField(
            model_name='fichatecnica',
            name='contenido',
        ),
        migrations.RemoveField(
            model_name='fichatecnica',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='fichatecnica',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='fichatecnica',
            name='horas',
        ),
        migrations.RemoveField(
            model_name='fichatecnica',
            name='instructor',
        ),
        migrations.RemoveField(
            model_name='fichatecnica',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='fichatecnica',
            name='objetivo',
        ),
        migrations.AddField(
            model_name='fichatecnica',
            name='curso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plancapacitacion.registrocurso'),
        ),
        migrations.AddField(
            model_name='fichatecnica',
            name='elementosDidacticos',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fichatecnica',
            name='fuentes',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fichatecnica',
            name='servicio',
            field=models.CharField(choices=[('Curso', 'Curso'), ('Taller', 'Taller')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ContenidoTematico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tema', models.CharField(max_length=200)),
                ('tiempo', models.IntegerField()),
                ('actividades', models.TextField()),
                ('fichaTecnica', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plancapacitacion.fichatecnica', verbose_name='Ficha Técnica')),
            ],
        ),
        migrations.CreateModel(
            name='CriterioEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criterio', models.CharField(max_length=200)),
                ('valor', models.IntegerField()),
                ('instrumento', models.CharField(max_length=200)),
                ('FichaTecnica', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plancapacitacion.fichatecnica', verbose_name='Ficha Técnica')),
            ],
        ),
    ]
