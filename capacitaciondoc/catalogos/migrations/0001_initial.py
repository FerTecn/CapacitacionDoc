# Generated by Django 5.1.1 on 2025-06-21 00:41

import catalogos.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CargoAutoridad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo_masculino', models.CharField(max_length=200)),
                ('cargo_femenino', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Cargos de Autoridad',
            },
        ),
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrera', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Carreras',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomenclatura', models.CharField(max_length=10, null=True)),
                ('numerodepartamento', models.CharField(max_length=54, null=True)),
                ('departamento', models.CharField(max_length=40)),
                ('nombreJefe', models.CharField(max_length=54, null=True)),
                ('apParternoJefe', models.CharField(max_length=40, null=True)),
                ('apMaternoJefe', models.CharField(max_length=40, null=True)),
                ('telefono', models.CharField(max_length=40, null=True)),
                ('email', models.CharField(max_length=60, null=True)),
                ('paginaWeb', models.CharField(max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='Dirigido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dirigido', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Dirigido a',
            },
        ),
        migrations.CreateModel(
            name='ExperienciaDocente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materia', models.CharField(max_length=40)),
                ('periodo', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='ExperienciaLaboral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puesto', models.CharField(max_length=40)),
                ('empresa', models.CharField(max_length=60)),
                ('fecha_inicio', models.DateField(null=True)),
                ('fecha_fin', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FormacionAcademica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institucion', models.CharField(max_length=40)),
                ('cedulaProf', models.CharField(max_length=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FormatoConstancia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.ImageField(upload_to=catalogos.models.formato_constancia_upload_path)),
                ('margend', models.ImageField(blank=True, null=True, upload_to=catalogos.models.formato_constancia_upload_path)),
                ('fondo', models.ImageField(blank=True, null=True, upload_to=catalogos.models.formato_constancia_upload_path)),
                ('footer', models.ImageField(blank=True, null=True, upload_to=catalogos.models.formato_constancia_upload_path)),
                ('year', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026)], default=2025)),
                ('vigente', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FormatoDepartamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.ImageField(upload_to=catalogos.models.formato_departamento_upload_path)),
                ('footer', models.ImageField(upload_to=catalogos.models.formato_departamento_upload_path)),
                ('year', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026)], default=2025)),
                ('vigente', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genero', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Genero',
            },
        ),
        migrations.CreateModel(
            name='GradoAcademico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grado', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name_plural': 'Grado académico',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.CharField(max_length=10, null=True)),
                ('fechaNac', models.DateField(null=True)),
                ('RFC', models.CharField(max_length=13, null=True)),
                ('telefono', models.CharField(max_length=10, null=True)),
            ],
            options={
                'verbose_name_plural': 'Instructores',
            },
        ),
        migrations.CreateModel(
            name='Lugar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreEdificio', models.CharField(max_length=40)),
                ('ubicacion', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name_plural': 'Lugares',
            },
        ),
        migrations.CreateModel(
            name='ParticipacionInstructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.CharField(max_length=40)),
                ('nombreEmpresa', models.CharField(max_length=40)),
                ('duracionHoras', models.IntegerField()),
                ('periodoInicio', models.DateField(null=True)),
                ('periodoFin', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerfilCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perfilCurso', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name_plural': 'Perfiles de Curso',
            },
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.TextField(max_length=50)),
                ('inicioPeriodo', models.DateField()),
                ('finPeriodo', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Periodos',
            },
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.CharField(max_length=15)),
                ('sede', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Sedes',
            },
        ),
        migrations.CreateModel(
            name='ValorCalificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valorCalificacion', models.CharField(max_length=40)),
                ('aprobatoria', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Valor de Calificación',
                'verbose_name_plural': 'Valores de Calificación',
            },
        ),
        migrations.CreateModel(
            name='Autoridad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('apPaterno', models.CharField(max_length=40)),
                ('apMaterno', models.CharField(max_length=40)),
                ('estatus', models.BooleanField()),
                ('firma', models.ImageField(blank=True, null=True, upload_to=catalogos.models.firma_autoridad_upload_path)),
                ('puesto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.cargoautoridad', verbose_name='Cargo')),
            ],
            options={
                'verbose_name_plural': 'Autoridades',
            },
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.CharField(max_length=10)),
                ('fechaNac', models.DateField(null=True)),
                ('RFC', models.CharField(max_length=13, null=True)),
                ('telefono', models.CharField(max_length=10, null=True)),
                ('departamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.departamento', verbose_name='Departamento')),
            ],
            options={
                'verbose_name_plural': 'Docentes',
            },
        ),
    ]
