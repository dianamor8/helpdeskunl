# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0007_auto_20150127_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Codigo_Bodega',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50)),
                ('equipo', models.ForeignKey(to='incidencia.Equipo')),
            ],
            options={
                'verbose_name': 'Codigo de Bodega',
                'verbose_name_plural': 'Codigos de Bodega',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='equipo',
            name='codigo_bodega',
        ),
    ]
