# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centro_asistencia', '0004_auto_20150806_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseConocimiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('titulo', models.CharField(max_length=250, verbose_name=b'T\xc3\xadtulo')),
                ('detalle', models.CharField(max_length=250, verbose_name=b'T\xc3\xadtulo')),
                ('tipo', models.CharField(max_length=100, verbose_name=b'Tipo', choices=[(b'0', b'Incidencia'), (b'1', b'Problema'), (b'2', b'Cambio')])),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name=b'Categor\xc3\xada', to='centro_asistencia.Servicio')),
            ],
            options={
                'verbose_name': 'Base de conocimiento',
                'verbose_name_plural': 'Bases de conocimientos',
            },
            bases=(models.Model,),
        ),
    ]
