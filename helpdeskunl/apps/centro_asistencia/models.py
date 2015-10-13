# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from helpdeskunl.apps.centro_asistencia.managers import *
from datetime import timedelta
from helpdeskunl.apps.home.current_user import get_current_user


class TimeStampedModel(models.Model):
	creado_en = models.DateTimeField(auto_now_add=True)
	actualizado_en = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)
	creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_requests_created', default=get_current_user)
	
	class Meta:
		abstract = True

class Estadistica_Sla(TimeStampedModel):
	tipo = models.CharField(max_length=150)
	minima_duracion = models.DurationField(null=True , blank=True)
	maxima_duracion = models.DurationField(null=True , blank=True)

	class Meta:
		verbose_name = "Estadistica SLA"
		verbose_name_plural = "Estadisticas SLA"
		db_table = 'EstadisticaSLA'
	def __unicode__(self):
		return u'%s'%(self.tipo)

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
	estadistica = models.ForeignKey(Estadistica_Sla, on_delete=models.DO_NOTHING)
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
		#http://codepen.io/anon/pen/WQpXJM
		#http://www.jqueryscript.net/form/Input-Number-Spinner-with-jQuery-Bootstrap-Spinner.html
		#http://www.jqueryscript.net/form/Touch-Friendly-jQuery-Input-Spinner-Plugin-For-Bootstrap-3-TouchSpin.html
		#www.virtuosoft.eu/code/bootstrap-touchspin/


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


