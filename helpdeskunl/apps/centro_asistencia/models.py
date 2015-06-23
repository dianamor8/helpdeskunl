# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from helpdeskunl.apps.centro_asistencia.managers import *

# Create your models here.

class Centro_Asistencia(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=250)	
	usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL)
	# NO ES NECESARIO AGREGAR UN TIPO DE USUARIO XQ ESO DEPENDE DEL GRUPO DE USUARIO AL QUE PERTENCE.
	objects = Centro_Asistencia_Manager()
	

	class Meta:
		verbose_name = "Centro de Asistencia"
		verbose_name_plural = "Centros de Asistencia"
		db_table = 'Centro_Asistencia'	
	def __unicode__(self):
		return u'%s'%(self.nombre)
	def get_absolute_url(self):
		return '/centro_asistencia/%i' %(self.id)	


class Servicio(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=250)
	centro = models.ForeignKey(Centro_Asistencia)
	class Meta:
		verbose_name = "Servicio"
		verbose_name_plural = "Servicios"
		db_table = 'Servicio'		
	def __unicode__(self):
		return u'%s'%(self.nombre)
	def get_absolute_url(self):
		return '/servicio/%i' %(self.id)

	def get_centro_asistencia(self):
		return '/centro_asistencia/%i' %(self.centro.id)

