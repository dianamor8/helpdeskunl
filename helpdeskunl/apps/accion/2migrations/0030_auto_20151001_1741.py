# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0029_auto_20151001_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada_recurso',
            name='conforme',
            field=models.BooleanField(default=True, choices=[(True, b'Si'), (False, b'No')]),
        ),
        migrations.AddField(
            model_name='entrada_recurso',
            name='observacion',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='entrada_recurso',
            name='detalle',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='entrada_recurso',
            name='nro_doc',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
