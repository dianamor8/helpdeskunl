# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.

#CREAR COMO CLASE PARA PORDER ASIGNAR USUARIOS A UN DEPARTAMENTO.
#AREA_SOPORTE = '0'	
#AREA_SISTEMAS = '1'
#AREA_REDES = '2'
#AREA_OTRO = '3'
#AREA_CHOICES = (
	#(AREA_SOPORTE, 'Mantenimiento de equipos e instalación de programas. Ej.: Reparación de impresoras, Instalación de Antivirus, etc.'),
	#(AREA_SISTEMAS, 'Problema de sistema informático institucional. Ej.: SGA, EVA, Biblioteca Virtual, etc.'),
	#(AREA_REDES, 'Instalaciones. Ej.: Falla de conexión a internet, etc.'),
	#(AREA_OTRO, 'Otro tipo de problema informático.'),
#)

class Dependencia(models.Model):
	detalle = models.CharField(max_length=250)
	class Meta:
		db_table = 'Dependencia'
		verbose_name = "Dependencia"
		verbose_name_plural = "Dependencias"
	def __unicode__(self):
		return u'%s - %s'%(self.id, self.detalle)

UR_BAJO='0'
UR_NORMAL='1'
UR_ALTO='2'
URGENCIA_CHOICES = (
	(UR_BAJO, 'Bajo'),
	(UR_NORMAL, 'Normal'),
	(UR_ALTO, 'Alto'),
)

ESTADO_NUEVA = '0'
ESTADO_ABIERTA = '1'
ESTADO_DELEGADA = '2'
ESTADO_ATENDIDA = '3'
ESTADO_DESPACHADA = '4'
ESTADO_PENDIENTE = '5'
ESTADO_CHOICES = (
	(ESTADO_NUEVA, 'Nueva incidencia'),
	(ESTADO_ABIERTA, 'Abrir incidencia'),
	(ESTADO_DELEGADA, 'Delegar incidencia'),
	(ESTADO_ATENDIDA, 'Atender incidencia'),
	(ESTADO_DESPACHADA, 'Cerrar incidencia'),
	(ESTADO_PENDIENTE, 'Incidencia pendiente'),	
)

class Incidencia(models.Model):

	titulo = models.CharField(max_length=100)	
	fecha = models.DateTimeField(auto_now=True)
	dependencia = models.ForeignKey('Dependencia')
	#area = models.CharField(choices=AREA_CHOICES, max_length=250)
	descripcion = models.CharField(max_length=50)
	urgencia = models.CharField(choices=URGENCIA_CHOICES, max_length=100) #Si selecciona URGENTE el campo justif_urgencia debe ser obligatorio
	justif_urgencia = models.CharField(null=True,max_length=150)
	prioridad_asignada = models.CharField(choices=URGENCIA_CHOICES, max_length=100, default=UR_NORMAL) #Este campo lo puede modificar el administrador
	estado = models.CharField(choices=ESTADO_CHOICES, max_length=100)

	class Meta:
		verbose_name = "Incidencia"
		verbose_name_plural = "Incidencias"
		db_table = ('Incidencia')
	def __unicode__(self):
		return self.titulo


