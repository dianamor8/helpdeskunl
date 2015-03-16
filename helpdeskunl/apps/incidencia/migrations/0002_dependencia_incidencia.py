# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dependencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
                ('detalle', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'Dependencia',
                'verbose_name': 'Dependencia',
                'verbose_name_plural': 'Dependencias',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Incidencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('descripcion', models.CharField(max_length=50)),
                ('urgencia', models.CharField(max_length=100, choices=[(b'0', b'Bajo'), (b'1', b'Normal'), (b'2', b'Alto')])),
                ('justif_urgencia', models.CharField(max_length=150, null=True)),
                ('prioridad_asignada', models.CharField(default=b'1', max_length=100, choices=[(b'0', b'Bajo'), (b'1', b'Normal'), (b'2', b'Alto')])),
                ('estado', models.CharField(max_length=100, choices=[(b'0', b'Nueva incidencia'), (b'1', b'Abrir incidencia'), (b'2', b'Delegar incidencia'), (b'3', b'Atender incidencia'), (b'4', b'Cerrar incidencia'), (b'5', b'Incidencia pendiente')])),
                ('dependencia', models.ForeignKey(to='incidencia.Dependencia')),
            ],
            options={
                'db_table': 'Incidencia',
                'verbose_name': 'Incidencia',
                'verbose_name_plural': 'Incidencias',
            },
            bases=(models.Model,),
        ),
    ]
