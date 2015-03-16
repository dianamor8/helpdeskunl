# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Centro_Asistencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'Centro_Asistencia',
                'verbose_name': 'Centro de Asistencia',
                'verbose_name_plural': 'Centros de Asistencia',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=250)),
                ('centro', models.ForeignKey(to='centro_asistencia.Centro_Asistencia')),
            ],
            options={
                'db_table': 'Servicio',
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
            },
            bases=(models.Model,),
        ),
    ]
