# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0022_solicitud_recurso_tecnico'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud_recurso',
            name='en_espera',
            field=models.CharField(default=b'0', max_length=2, verbose_name=b'Espera', choices=[(b'0', b'SI'), (b'1', b'NO')]),
        ),
    ]
