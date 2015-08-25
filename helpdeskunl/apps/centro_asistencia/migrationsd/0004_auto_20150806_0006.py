# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('centro_asistencia', '0003_auto_20150715_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal_operativo',
            name='grupo',
            field=models.ForeignKey(to='auth.Group', on_delete=django.db.models.deletion.DO_NOTHING),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personal_operativo',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.DO_NOTHING),
            preserve_default=True,
        ),
    ]
