# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accion', '0012_auto_20150923_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud_recurso',
            name='tecnico',
            # field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, default=datetime.datetime(2015, 9, 26, 18, 1, 6, 516697, tzinfo=utc), to=settings.AUTH_USER_MODEL),
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
