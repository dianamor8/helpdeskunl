# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0008_auto_20150128_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detalle_Equipos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo_bodega', models.ForeignKey(to='incidencia.Codigo_Bodega')),
                ('equipo', models.ForeignKey(to='incidencia.Equipo')),
                ('incidencia', models.ForeignKey(to='incidencia.Incidencia')),
            ],
            options={
                'verbose_name': 'Detalle_Equipos',
                'verbose_name_plural': 'Detalle_Equiposs',
            },
            bases=(models.Model,),
        ),
    ]
