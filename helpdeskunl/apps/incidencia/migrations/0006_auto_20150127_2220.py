# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0005_auto_20150127_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='codigo_bodega',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
