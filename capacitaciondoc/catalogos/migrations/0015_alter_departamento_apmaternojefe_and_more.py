# Generated by Django 5.1.4 on 2025-02-08 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0014_alter_docente_departamento_alter_docente_fechanac_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamento',
            name='apMaternoJefe',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='apParternoJefe',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='email',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='nombreJefe',
            field=models.CharField(max_length=54, null=True),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='nomenclatura',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='numerodepartamento',
            field=models.CharField(max_length=54, null=True),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='paginaWeb',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='telefono',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='periodo',
            name='clave',
            field=models.TextField(max_length=50),
        ),
    ]
