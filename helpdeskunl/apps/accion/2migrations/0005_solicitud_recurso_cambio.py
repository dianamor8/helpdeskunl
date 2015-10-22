# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cambio', '0004_remove_cambio_solicitud_recurso'),
        ('accion', '0004_auto_20150921_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud_recurso',
            name='cambio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='cambio.Cambio', null=True),
        ),
    ]
