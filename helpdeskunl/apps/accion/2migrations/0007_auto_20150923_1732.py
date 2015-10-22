# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0006_auto_20150923_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostico_inicial',
            name='incidencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='incidencia.Incidencia'),
        ),
    ]
