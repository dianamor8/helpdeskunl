# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0026_remove_solicitud_recurso_en_espera'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada_recurso',
            name='detalle',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='solicitud_recurso',
            name='despachado',
            field=models.BooleanField(default=False, choices=[(True, b'Si'), (False, b'No')]),
        ),
        migrations.AlterField(
            model_name='solicitud_recurso',
            name='esperar',
            field=models.BooleanField(default=True, choices=[(True, b'Si'), (False, b'No')]),
        ),
        migrations.AlterField(
            model_name='solicitud_recurso',
            name='notificar_email',
            field=models.BooleanField(default=False, choices=[(True, b'Si'), (False, b'No')]),
        ),
    ]
