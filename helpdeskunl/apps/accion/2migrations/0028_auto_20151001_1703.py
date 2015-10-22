# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0027_auto_20151001_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada_recurso',
            name='solicitud_recurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='accion.Solicitud_Recurso', null=True),
        ),
    ]
