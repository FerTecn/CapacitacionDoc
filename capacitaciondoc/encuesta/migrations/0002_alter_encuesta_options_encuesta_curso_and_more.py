# Generated by Django 5.1.4 on 2025-01-31 04:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0001_initial'),
        ('plancapacitacion', '0002_alter_registrocurso_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='encuesta',
            options={'verbose_name_plural': 'Encuestas'},
        ),
        migrations.AddField(
            model_name='encuesta',
            name='curso',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='encuestas', to='plancapacitacion.registrocurso'),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='docente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='encuestas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='fecha_realizacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='encuesta',
            unique_together={('docente', 'curso')},
        ),
    ]
