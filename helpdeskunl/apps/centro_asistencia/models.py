# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from helpdeskunl.apps.centro_asistencia.managers import *
from datetime import timedelta

class Centro_Asistencia(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=250)	
	estado = models.BooleanField(default=True)
	usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Personal_Operativo')

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
	centro = models.ForeignKey(Centro_Asistencia, on_delete=models.CASCADE)
	t_minimo = models.DurationField()
	t_normal = models.DurationField()
	t_maximo = models.DurationField()
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


class Personal_Operativo(models.Model):
	centro_asistencia = models.ForeignKey(Centro_Asistencia, on_delete=models.DO_NOTHING)
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)    
	grupo = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
	class Meta:
		verbose_name = "Personal Operativo"
		verbose_name_plural = "Personal Operativo"
		db_table = 'Personal_Operativo'
	def __unicode__(self):
		return u'[%s, %s, %s]'%(self.centro_asistencia.id, self.usuario.dni, self.grupo.name)


#CALCULO DE TIEMPOS
# >>> s.sopor_fecha = datetime.now()
# >>> s.sopor_fin = datetime.now()
# >>> diff = s.sopor_fin - s.sopor_fecha
# >>> print 'Dif en segundos %s ' %(diff.seconds)  
# Dif en segundos 4 
# >>> 
# MEMCACHÉ O REDIS PARA almacenar campos calculados
# CALCULO DEL TIEMPO TRANSCURRIDO http://es.wikihow.com/calcular-el-tiempo-transcurrido
# CAMPO EXTRA http://www.elornitorrincoenmascarado.com/2015/02/django-tip-modificar-la-sentencias-sql.html


