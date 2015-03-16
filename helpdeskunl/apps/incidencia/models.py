# -*- coding: utf-8 -*-
from django.db import models

#Para categorizar producto con falla
class Categoria_Equipo(models.Model):
	nombre = models.CharField(max_length=100)
	class Meta:
		verbose_name = "Categoria del equipo"
		verbose_name_plural = "Categorias"
		db_table = 'Categoria_Equipo'
	def __unicode__(self):
		return self.nombre

#Determina la marca del equipo
class Marca_Equipo(models.Model):
	nombre = models.CharField(max_length=100)
	class Meta:
		verbose_name = "Marca"
		verbose_name_plural = "Marcas"
		db_table = 'Marca_Equipo'
	def __unicode__(self):
		return self.nombre

#
class Equipo(models.Model):	
	categoria = models.ForeignKey('Categoria_Equipo') #Impresora, Infocus, 
	marca = models.ForeignKey('Marca_Equipo') #epson, genius
	modelo = models.CharField(max_length=250, null=True, blank=True) #12345, 1232131	
	class Meta:
		verbose_name = "Equipo"
		verbose_name_plural = "Lista de equipos"
		db_table = 'Equipo'
	def __unicode__(self):
		return u'%s %s %s'%(self.categoria, self.marca, self.modelo)

#Para el registro de códigos de bodega de los equipos de la UNL
class Codigo_Bodega(models.Model):
	codigo = models.CharField(max_length=50)
	equipo = models.ForeignKey('Equipo')
	class Meta:
		verbose_name = "Codigo de Bodega"
		verbose_name_plural = "Codigos de Bodega"
	def __unicode__(self):
		return u'%s - %s'%(self.equipo, self.codigo)

class Detalle_Equipos(models.Model):
	codigo_bodega = models.ForeignKey('Codigo_Bodega', null=True, blank=True)
	equipo = models.ForeignKey('Equipo')
	incidencia = models.ForeignKey('Incidencia')
	class Meta:
		verbose_name = "Detalle Equipo"
		verbose_name_plural = "Detalle de Equipos"
	def __unicode__(self):
		return u'%s %s %s'%(self.codigo_bodega, self.equipo, self.incidencia)
    

# Create your models here.
class Dependencia(models.Model):
	nombre = models.CharField(max_length=250)
	detalle = models.CharField(max_length=250)
	class Meta:
		db_table = 'Dependencia'
		verbose_name = "Dependencia"
		verbose_name_plural = "Dependencias"
	def __unicode__(self):
		return u'%s. %s'%(self.id, self.nombre)

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
	descripcion = models.CharField(max_length=50)
	urgencia = models.CharField(choices=URGENCIA_CHOICES, max_length=100) #Si selecciona URGENTE el campo justif_urgencia debe ser obligatorio
	justif_urgencia = models.CharField(null=True,max_length=150)
	prioridad_asignada = models.CharField(choices=URGENCIA_CHOICES, max_length=100, default=UR_NORMAL) #Este campo lo puede modificar el administrador
	estado = models.CharField(choices=ESTADO_CHOICES, max_length=100)	
	#ES ASIGNADO A MUCHOS USUARIOS OPERADORES
	class Meta:
		verbose_name = "Incidencia"
		verbose_name_plural = "Incidencias"
		db_table = ('Incidencia')
	def __unicode__(self):
		return self.titulo

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