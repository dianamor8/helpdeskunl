# -*- coding: utf-8 -*-
from django.db import models
from helpdeskunl.apps.centro_asistencia.models import *

class TimeStampedModel(models.Model):
	creado_en = models.DateTimeField(auto_now_add=True)
	actualizado_en = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)
	
	class Meta:
		abstract = True


INCIDENCIA='0'
PROBLEMA='1'
CAMBIO='2'
TIPO_GESTION = (
	(INCIDENCIA, 'Incidencia'),
	(PROBLEMA, 'Problema'),
	(CAMBIO, 'Cambio'),
)
# Create your models here.
class BaseConocimiento(TimeStampedModel):


	titulo = models.CharField(max_length=250, verbose_name='Título')
	detalle = models.CharField(max_length=250, verbose_name='Título')
	tipo = models.CharField(choices=TIPO_GESTION, max_length=100, verbose_name='Tipo')# ENTRADA DE LA BASE DE CONOCIMIENTO POR TIPOS	
	# servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING, verbose_name='Categoría')# DETERMINA AL TIPO DE SERVICIO


	# DETERMINA A QUE CENTRO DE ASISTENCIA PERTENCE LA ENTRADA
	# centro_asistencia = models.ForeignKey(Centro_Asistencia, on_delete=models.DO_NOTHING)
	class Meta:
		verbose_name = "Base de conocimiento"
		verbose_name_plural = "Bases de conocimientos"