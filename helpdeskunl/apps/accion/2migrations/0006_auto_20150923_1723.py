# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import helpdeskunl.apps.home.current_user
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('incidencia', '__first__'),
        ('accion', '0005_solicitud_recurso_cambio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnostico_Bien',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('recibido', models.BooleanField(default=False)),
                ('verificado', models.BooleanField(default=False)),
                ('bien', models.ForeignKey(to='incidencia.Bien', on_delete=django.db.models.deletion.DO_NOTHING)),
                ('creado_por', models.ForeignKey(related_name='diagnostico_bien_requests_created', default=helpdeskunl.apps.home.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Diagnostico_Bien',
                'verbose_name': 'Diagnostico_Bien',
                'verbose_name_plural': 'Diagnostico_Bienes',
            },
        ),
        migrations.CreateModel(
            name='Diagnostico_Inicial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('diagnostico', models.CharField(max_length=250)),
                ('bienes_recibidos', models.ManyToManyField(to='incidencia.Bien', through='accion.Diagnostico_Bien', blank=True)),
                ('creado_por', models.ForeignKey(related_name='diagnostico_inicial_requests_created', default=helpdeskunl.apps.home.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
                ('incidencia', models.ForeignKey(to='incidencia.Incidencia', on_delete=django.db.models.deletion.DO_NOTHING)),
                ('tecnico', models.ForeignKey(related_name='tecnico', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Diagnostico_Inicial',
                'verbose_name': 'Diagnostico Inicial',
                'verbose_name_plural': 'Diagnosticos Inicial',
            },
        ),
        migrations.AddField(
            model_name='diagnostico_bien',
            name='diagnostico',
            field=models.ForeignKey(to='accion.Diagnostico_Inicial', on_delete=django.db.models.deletion.DO_NOTHING),
        ),
    ]
