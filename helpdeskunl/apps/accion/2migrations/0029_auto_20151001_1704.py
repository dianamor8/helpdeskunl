# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0028_auto_20151001_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada_recurso',
            name='usuario_registra',
            field=models.ForeignKey(related_name='usuario_registra', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
