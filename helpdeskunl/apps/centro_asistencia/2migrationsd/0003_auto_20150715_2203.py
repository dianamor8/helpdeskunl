# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centro_asistencia', '0002_auto_20150711_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='centro_asistencia',
            name='estado',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personal_operativo',
            name='centro_asistencia',
            field=models.ForeignKey(to='centro_asistencia.Centro_Asistencia', on_delete=django.db.models.deletion.DO_NOTHING),
            preserve_default=True,
        ),
    ]
