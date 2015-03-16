# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0002_dependencia_incidencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria_Equipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Categoria_Equipo',
                'verbose_name': 'Categoria del equipo',
                'verbose_name_plural': 'Lista de categorias',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modelo', models.CharField(max_length=250)),
                ('codigo_bodega', models.CharField(max_length=50)),
                ('categoria', models.ForeignKey(to='incidencia.Categoria_Equipo')),
            ],
            options={
                'verbose_name': 'Equipo',
                'verbose_name_plural': 'Lista de equipos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Marca_Equipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Marca_Equipo',
                'verbose_name': 'Categoria del equipo',
                'verbose_name_plural': 'Lista de categorias',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='equipo',
            name='marca',
            field=models.ForeignKey(to='incidencia.Marca_Equipo'),
            preserve_default=True,
        ),
    ]
