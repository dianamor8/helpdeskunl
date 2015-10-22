# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_perfil_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='avatar',
        ),
    ]
