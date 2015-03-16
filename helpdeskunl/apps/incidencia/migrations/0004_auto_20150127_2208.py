# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0003_auto_20150127_2207'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='equipo',
            table='Equipo',
        ),
    ]
