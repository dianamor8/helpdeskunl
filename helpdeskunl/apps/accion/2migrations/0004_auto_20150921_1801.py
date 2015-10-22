# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0003_auto_20150921_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accion',
            name='solicitud_recurso',
        ),
        migrations.AddField(
            model_name='solicitud_recurso',
            name='accion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='accion.Accion', null=True),
        ),
    ]
