# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from helpdeskunl.apps.centro_asistencia.models import *
from helpdeskunl.apps.usuarios.models import *
from helpdeskunl.apps.home.current_user import get_current_user
from django.core.urlresolvers import reverse
# TIEMPO
from datetime import datetime
from django.utils import timezone


class TimeStampedModel(models.Model):
	creado_en = models.DateTimeField(auto_now_add=True)
	actualizado_en = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)
	creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_requests_created', default=get_current_user)
	
	class Meta:
		abstract = True

	# def save(self):
	# 	self.creado_por = self.request.user
	# 	super(TimeStampedModel, self).save()

INDIVIDUAL='0'
COMPONENTE='1'
TIPO_CHOICES = (
	(INDIVIDUAL, 'INDIVIDUAL'),
	(COMPONENTE, 'COMPONENTE'),
)
class Bien(TimeStampedModel):
	codigo = models.CharField(max_length=250, verbose_name='Código Institucional', null=True, blank=True, unique=True)
	codigo_cfn = models.CharField(max_length=250, verbose_name='Código CFN', null=True, blank=True, unique=True)
	serie = models.CharField(max_length=250, verbose_name='Serie', unique=True)
	producto = models.CharField(max_length=100, verbose_name='Equipo')	
	validado = models.BooleanField(default=False)
	tipo = models.CharField(choices=TIPO_CHOICES, max_length=100, verbose_name='Ingreso')
	padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
	custodio = models.ForeignKey(settings.AUTH_USER_MODEL)
	
	class Meta:
		verbose_name = "Bien Institucional"
		verbose_name_plural = "Bienes Institucionales"
		db_table = "Bien"	
	
	def __unicode__(self):
		caracteristicas = ""
		c = self.caracteristica_bien_set		
		for caracteristica in c.all():
			caracteristicas += str(caracteristica.detalle) + ","
		return '%s:%s [%s]'%(self.codigo, self.producto, caracteristicas)

MARCA='0'
MODELO='1'
COLOR='2'
OTRO='3'
CARACTERISTICAS_CHOICES = (
	(MARCA, 'Marca'),
	(MODELO, 'Modelo'),
	(COLOR, 'Color'),
	(OTRO, 'Otro'),
)
class Caracteristica_Bien(TimeStampedModel):
	tipo = models.CharField(choices=CARACTERISTICAS_CHOICES, max_length=100, verbose_name='Caracteristica')
	detalle = models.CharField(max_length=100, verbose_name='Detalle')
	bien = models.ForeignKey(Bien, on_delete=models.CASCADE)
	class Meta:
		verbose_name = "Caracteristica"
		verbose_name_plural = "Caracteristicas del Bien"
		db_table = "Caracteristicas_Bien"
	def __unicode__(self):
		return '%s - %s'%(self.tipo, self.detalle)

BAJO='0'
MEDIO='1'
CRITICO='2'

PRIORIDAD_DETERMINADA_CHOICES = (
	(CRITICO, 'Crítico'),
	(MEDIO, 'Medio'),
	(BAJO, 'Bajo'),
)

UR_BAJO='0'
UR_NORMAL='1'
UR_ALTO='2'
URGENCIA_CHOICES = (
	(UR_BAJO, 'Bajo'),
	(UR_NORMAL, 'Normal'),
	(UR_ALTO, 'Alto'),
)

N_INCIDENCIA='0'
N_PROBLEMA='1'
N_CAMBIO='2'
NIVELES_CHOICES = (
	(N_INCIDENCIA, 'Incidencia'),
	(N_PROBLEMA, 'Problema'),
	(N_CAMBIO, 'Cambio'),
)

ESTADO_NUEVA = '0'
ESTADO_DELEGADA = '1'
ESTADO_ABIERTA = '2'
ESTADO_ATENDIDA = '3'
ESTADO_PENDIENTE = '4'
ESTADO_CHOICES = (
	(ESTADO_NUEVA, 'Nueva'),
	(ESTADO_DELEGADA, 'Asignada'),
	(ESTADO_ABIERTA, 'Atendiendo'),	
	(ESTADO_ATENDIDA, 'Cerrada'),	
	(ESTADO_PENDIENTE, 'Pendiente'),	
)

class Incidencia(TimeStampedModel):
		
	def url(self, filename):
		ruta = "MultimediaData/Incidencia/%s/%s"%(self.centro_asistencia.id, str(filename))
		return ruta

	fecha = models.DateTimeField(null=True , blank=True , verbose_name='fecha de asignación')
	titulo = models.CharField(max_length=100)	
	descripcion = models.CharField(max_length=50)
	solicitante = models.ForeignKey(settings.AUTH_USER_MODEL,default=get_current_user, related_name='usuario_solicitante')
	prioridad_solicitada = models.CharField(choices=URGENCIA_CHOICES, max_length=100, default=UR_NORMAL) #Si selecciona URGENTE el campo justif_urgencia debe ser obligatorio
	justif_urgencia = models.CharField(null=True,max_length=150, blank=True)
	prioridad_asignada = models.CharField(choices=URGENCIA_CHOICES, max_length=100) #Este campo lo puede modificar el administrador
	estado_incidencia = models.CharField(choices=ESTADO_CHOICES, max_length=100, default=ESTADO_NUEVA)
	nivel = models.CharField(choices=NIVELES_CHOICES, max_length=100, default=N_INCIDENCIA)	
	centro_asistencia = models.ForeignKey(Centro_Asistencia)
	servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING, null=True, blank=True)	
	bienes = models.ManyToManyField(Bien, blank=True)
	imagen = models.ImageField(upload_to=url,help_text='Seleccione una imagen.', null=True, blank=True, max_length=300)
	#ES ASIGNADO A MUCHOS USUARIOS OPERADORES	
	# tecnicos = models.ManyToManyField("self", symmetrical=False, through= 'Asignacion_Incidencia')
	tecnicos = models.ManyToManyField(Perfil, through= 'Asignacion_Incidencia', through_fields = ('incidencia','tecnico'))
	ejecucion = models.CharField(choices=PRIORIDAD_DETERMINADA_CHOICES, max_length=100, null=True , blank=True)
	duracion = models.DurationField(null=True , blank=True)
	# agregar la fecha que caduca
	caduca = models.DateTimeField(null=True , blank=True)	
	class Meta:
		verbose_name = "Incidencia"
		verbose_name_plural = "Incidencias"
		db_table = ('Incidencia')
	
	def __unicode__(self):
		return self.titulo

	def get_class_estado(self):		
		switcher = {
			0: "btn-success", #Nueva
			1: "btn-info", #Atendiendo
			2: "btn-primary", #Atendida
			3: "btn-danger", #Cerrada
			4: "btn-warning", #Pendiente
		}		
		return switcher.get(int(self.estado_incidencia))

	def get_absolute_url(self):
		return reverse('incidencia_update', kwargs={'pk': self.pk})

	def add_bienes(self, args):
		for bien in args:
			self.bienes.add(bien)

	def remove_bienes(self, args):
		for bien in args:
			self.bienes.remove(bien)

	def get_class_prioridad_solicitada(self):		
		switcher = {
			0: "btn btn-default", #Bajo
			1: "btn btn-success", #Normal
			2: "btn btn-danger", #Alto			
		}		
		return switcher.get(int(self.prioridad_solicitada))

	def get_class_prioridad_asignada_table(self):		
		switcher = {
			0: "label label-default", #Bajo
			1: "label label-success", #Normal
			2: "label label-danger", #Alto			
		}		
		return switcher.get(int(self.prioridad_asignada))


	def get_class_prioridad_asignada(self):		
		switcher = {
			0: "btn btn-default", #Bajo
			1: "btn btn-success", #Normal
			2: "btn btn-danger", #Alto			
		}		
		return switcher.get(int(self.prioridad_asignada))

	def get_gestion(self):		
		switcher = {
			0: "Gestión de incidentes", #Bajo
			1: "Gestión de problemas", #Normal
			2: "Gestión de cambios", #Alto			
		}		
		return switcher.get(int(self.nivel))

	# CALCULO DE PRIORIDAD
	def determinar_prioridad(self):
		
		if self.prioridad_solicitada == '0':
			if self.prioridad_asignada == '0':
				return BAJO
			if self.prioridad_asignada == '1':
				return MEDIO
			if self.prioridad_asignada == '2':
				return MEDIO
		if self.prioridad_solicitada == '1':
			if self.prioridad_asignada == '0':
				return MEDIO
			if self.prioridad_asignada == '1':
				return MEDIO
			if self.prioridad_asignada == '2':
				return MEDIO		
		if self.prioridad_solicitada == '2':
			if self.prioridad_asignada == '0':
				return MEDIO
			if self.prioridad_asignada == '1':
				return MEDIO
			if self.prioridad_asignada == '2':
				return CRITICO

	def determinar_duracion(self):
		if self.ejecucion == '2': #CRITICO
			return self.servicio.t_minimo
		if self.ejecucion == '1': #MEDIO
			return self.servicio.t_normal
		if self.ejecucion == '0': #BAJO
			return self.servicio.t_maximo
 
	def calcular_caducidad(self):
		fecha_inicio = self.fecha
		duracion = self.duracion		
		return fecha_inicio + duracion

	def es_vigente(self, request):
		hoy = timezone.now()
		if self.caduca is None:
			return True

		if self.caduca < hoy:
			self.estado_incidencia = '3'
			self.save()
			if not self.cierre_incidencia_set.all():
				cierre = Cierre_Incidencia(tipo='0', usuario=request.user, observacion='Cierre automático por expiración.', incidencia=self)
				cierre.save()
			return False
		else:
			return True



class Asignacion_Incidencia(TimeStampedModel):
	incidencia = models.ForeignKey(Incidencia, on_delete=models.DO_NOTHING)
	tecnico = models.ForeignKey(settings.AUTH_USER_MODEL)
	administrador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='usuario_desde')
	observacion = models.CharField(max_length=150, blank=True, null=True)
	fecha_asignacion = models.DateTimeField(auto_now_add=True)	
	class Meta:
		verbose_name = "Asignacion de Incidencia"
		verbose_name_plural = "Asignaciones de Incidencias"
		db_table = 'Asignacion_Incidencia'




CREA_INCIDENCIA = '0'
ASIGNA_INCIDENCIA = '1'
ABRE_INCIDENCIA = '2'
CREA_SOLICITUD_RECURSO = '3'
ASIGNACION_RECURSO = '4'
CREA_PROBLEMA = '5'
ASIGNACION_RECURSO_PROBLEMA = '6'

HISTORIAL_CHOICES = (
	(CREA_INCIDENCIA, 'CREAR INCIDENCIA'),
	(ASIGNA_INCIDENCIA, 'ASIGNAR INCIDENCIA'),
	(ABRE_INCIDENCIA, 'ABRIR INCIDENCIA'),	
	(CREA_SOLICITUD_RECURSO, 'CREAR RECURSO'),	
	(ASIGNACION_RECURSO, 'ASIGNA RECURSO'),	
	(CREA_PROBLEMA, 'CREAR PROBLEMA'),	
	(ASIGNACION_RECURSO_PROBLEMA, 'ASIGNAR RECURSO PROBLEMA'),	
)
class Historial_Incidencia(TimeStampedModel):
	incidencia = models.ForeignKey(Incidencia, on_delete=models.DO_NOTHING)
	tipo = models.CharField(choices=HISTORIAL_CHOICES, max_length=2)
	fecha = models.DateField(null=True , blank=True)
	tiempo_restante = models.DurationField(null=True , blank=True)

	class Meta:
		verbose_name = "Historial de Incidencia"
		verbose_name_plural = "Historial de Incidencia"
		db_table = 'Historial_Incidencia'


CIERRE_AUTOMATICO = '0'
CIERRE_MANUAL = '1'
CIERRE_CHOICES = (
	(CIERRE_AUTOMATICO, 'CIERCierre_Incidencia AUTOMÁTICO'),
	(CIERRE_MANUAL, 'CIERRE MANUAL'),
)
class Cierre_Incidencia(TimeStampedModel):
	incidencia = models.ForeignKey(Incidencia, on_delete=models.DO_NOTHING)
	tipo = models.CharField(choices=CIERRE_CHOICES, max_length=2)	
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
	observacion = models.CharField(max_length=250)

	class Meta:
		verbose_name = "Cierre de Incidencia"
		verbose_name_plural = "Cierres de Incidencia"
		db_table = 'Cierre_Incidencia'

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