# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from helpdeskunl.apps.centro_asistencia.models import *
from helpdeskunl.apps.usuarios.models import *
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.accion.models import *
from helpdeskunl.apps.cambio.models import *

from helpdeskunl.apps.home.current_user import get_current_user
from django.core.urlresolvers import reverse

# Create your models here.
class TimeStampedModel(models.Model):
	creado_en = models.DateTimeField(auto_now_add=True)
	actualizado_en = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)
	creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_requests_created', default=get_current_user)
	
	class Meta:
		abstract = True


ABIERTO='0'
CERRADO='1'
ESTADO_PROBLEMA_CHOICES = (
	(ABIERTO, 'ABIERTO'),
	(CERRADO, 'CERRADO'),
)
class Problema(TimeStampedModel):
	titulo = models.CharField(max_length=100, verbose_name='Titulo')
	descripcion = models.CharField(max_length=250, verbose_name='Causa')
	solucion = models.CharField(max_length=250, verbose_name='Solucion')
	estado_problema = models.CharField(choices=ESTADO_PROBLEMA_CHOICES, max_length=2, verbose_name='Estado Problema')
	incidencia = models.ForeignKey(Incidencia, on_delete=models.DO_NOTHING)
	bien = models.ForeignKey(Bien, blank=True, null=True)	
	fecha_apertura = models.DateTimeField(null=True , blank=True , verbose_name='fecha de apertura') #CUANDO EL ADMINISTRADOR PIDE EL CAMBIO
	fecha_solucion = models.DateTimeField(null=True , blank=True , verbose_name='fecha de solcion') #CUANDO EL ADMINISTRADOR RESPONDE POR EL CAMBIO
	fecha_atencion = models.DateTimeField(null=True , blank=True , verbose_name='fecha de atención') #CUANDO EL TECNICO EMPIEZA A TRABAJAR DE NEUVO EN LA INCIDENCIA
	administrador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='administrador',null=True , blank=True ,)	#ADMINISTRADOR QUE ATIENDE EL PROBLEMA / NULL TRUE HASTA QUE UN ADMINISTRADOR ABRA EL PROBLEMA 
	tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)	#TÉCNICO QUE ATIENDE CREA NUEVO PROBLEMA
	
	class Meta:
		verbose_name = "Problema"
		verbose_name_plural = "Problemas"
		db_table = "Problema"
	def __unicode__(self):
		return '%s - %s'%(self.titulo, self.incidencia)