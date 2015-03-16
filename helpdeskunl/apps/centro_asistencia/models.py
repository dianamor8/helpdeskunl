# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Centro_Asistencia(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=250)
	class Meta:
		verbose_name = "Centro de Asistencia"
		verbose_name_plural = "Centros de Asistencia"
		db_table = 'Centro_Asistencia'	
	def __unicode__(self):
		return u'%s'%(self.nombre)


class Servicio(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=250)
	centro = models.ForeignKey('Centro_Asistencia')
	class Meta:
		verbose_name = "Servicio"
		verbose_name_plural = "Servicios"
		db_table = 'Servicio'
	def __unicode__(self):
		return u'%s'%(self.nombre)