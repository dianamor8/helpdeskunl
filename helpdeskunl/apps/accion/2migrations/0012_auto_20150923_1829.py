# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0011_auto_20150923_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostico_inicial',
            name='tecnico',
            field=models.ForeignKey(related_name='tecnico', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
