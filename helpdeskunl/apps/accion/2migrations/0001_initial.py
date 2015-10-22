# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import helpdeskunl.apps.home.current_user
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cambio', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('incidencia', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('titulo', models.CharField(max_length=100, verbose_name=b'Titulo')),
                ('descripcion', models.CharField(max_length=250, verbose_name=b'Descripci\xc3\xb3n')),
                ('visible_usuario', models.BooleanField(default=True)),
                ('nivel', models.CharField(max_length=2, choices=[(b'0', b'Incidencia'), (b'1', b'Problema'), (b'2', b'Cambio')])),
                ('cambio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='cambio.Cambio', null=True)),
                ('creado_por', models.ForeignKey(related_name='accion_requests_created', default=helpdeskunl.apps.home.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
                ('incidencia', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='incidencia.Incidencia', null=True)),
            ],
            options={
                'db_table': 'Accion',
                'verbose_name': 'Accion',
                'verbose_name_plural': 'Acciones',
            },
        ),
        migrations.CreateModel(
            name='Entrada_Recurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('nro_doc', models.CharField(max_length=50)),
                ('detalle', models.CharField(max_length=50)),
                ('creado_por', models.ForeignKey(related_name='entrada_recurso_requests_created', default=helpdeskunl.apps.home.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
                ('nuevo_bien', models.ForeignKey(blank=True, to='incidencia.Bien', null=True)),
            ],
            options={
                'db_table': 'Entrada_Recurso',
                'verbose_name': 'Entrada de Recurso',
                'verbose_name_plural': 'Entrada de Recursos',
            },
        ),
        migrations.CreateModel(
            name='Solicitud_Recurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('tipo', models.CharField(max_length=2, verbose_name=b'Tipo de Recurso', choices=[(b'0', b'PIEZA'), (b'1', b'PARTE'), (b'2', b'REPOSICION'), (b'3', b'GARANTIA'), (b'4', b'OTRO')])),
                ('recurso', models.CharField(max_length=250, verbose_name=b'detalle')),
                ('despachado', models.BooleanField(default=False)),
                ('bien', models.ForeignKey(blank=True, to='incidencia.Bien', null=True)),
                ('creado_por', models.ForeignKey(related_name='solicitud_recurso_requests_created', default=helpdeskunl.apps.home.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Solicitud_Recurso',
                'verbose_name': 'Solicitud de Recurso',
                'verbose_name_plural': 'Solicitud de Recursos',
            },
        ),
        migrations.AddField(
            model_name='entrada_recurso',
            name='solicitud_recurso',
            field=models.ForeignKey(to='accion.Solicitud_Recurso', on_delete=django.db.models.deletion.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='entrada_recurso',
            name='usuario_registra',
            field=models.ForeignKey(related_name='usuario_registra', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
