# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0009_detalle_equipos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detalle_equipos',
            options={'verbose_name': 'Detalle Equipo', 'verbose_name_plural': 'Detalle de Equipos'},
        ),
        migrations.AlterField(
            model_name='detalle_equipos',
            name='codigo_bodega',
            field=models.ForeignKey(blank=True, to='incidencia.Codigo_Bodega', null=True),
            preserve_default=True,
        ),
    ]
