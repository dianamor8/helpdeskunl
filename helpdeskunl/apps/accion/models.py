# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from helpdeskunl.apps.centro_asistencia.models import *
from helpdeskunl.apps.usuarios.models import *
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.problema.models import *
from helpdeskunl.apps.cambio.models import *
from helpdeskunl.apps.home.models import *

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


PIEZA='0'
PARTE='1'
REPOSICION='2'
GARANTIA='3'
OTRO='4'

TIPO_SOLICITUD_CHOICES = (
	(PIEZA, 'PIEZA'),
	(PARTE, 'PARTE'),
	(REPOSICION, 'REPOSICION'),
	(GARANTIA, 'GARANTIA'),
	(OTRO, 'OTRO'),
)


class Accion(TimeStampedModel):
	titulo = models.CharField(max_length=100, verbose_name='Titulo')	
	descripcion = models.CharField(max_length=250, verbose_name='Descripción')		
	visible_usuario= models.BooleanField(default=True)	
	nivel = models.CharField(choices=NIVELES_CHOICES, max_length=2)	
	problema = models.ForeignKey(Problema, on_delete=models.DO_NOTHING, blank=True, null=True)
	incidencia = models.ForeignKey(Incidencia, on_delete=models.DO_NOTHING, blank=True, null=True)
	cambio = models.ForeignKey(Cambio, on_delete=models.DO_NOTHING, blank=True, null=True)
	tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)	#TÉCNICO QUE CREA LA ACCION

	class Meta:
		verbose_name = "Accion"
		verbose_name_plural = "Acciones"
		db_table = "Accion"
	def __unicode__(self):
		return '%s - %s'%(self.titulo, self.incidencia)


BOOL_CHOICES = ((True, 'Si'), (False, 'No'))
class Solicitud_Recurso(TimeStampedModel):
	
	tipo = models.CharField(choices=TIPO_SOLICITUD_CHOICES, max_length=2, verbose_name='Tipo de Recurso')
	proveedor = models.ForeignKey(Contacto, on_delete=models.DO_NOTHING, blank=True, null=True) # CUANDO LA SOLICITUD VIENE DIRECTO DE ACCION AGREGAR EL PROVEEDOR, SI VIENE DE UN PROBLEMA 
	recurso = models.CharField(max_length=250, verbose_name='detalle')	
	accion = models.ForeignKey(Accion, on_delete=models.DO_NOTHING, blank=True, null=True)
	cambio = models.ForeignKey(Cambio, on_delete=models.DO_NOTHING, blank=True, null=True)
	bien = models.ForeignKey(Bien, blank=True, null=True)	
	despachado = models.BooleanField(default=False,  choices=BOOL_CHOICES)
	tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)	
	esperar = models.BooleanField(default=True, choices=BOOL_CHOICES)
	notificar_email = models.BooleanField(default=False, choices=BOOL_CHOICES)
	
	class Meta:
		verbose_name = "Solicitud de Recurso"
		verbose_name_plural = "Solicitud de Recursos"
		db_table = "Solicitud_Recurso"
	def __unicode__(self):
		return self.recurso

# CLASS ENTRADA DE RECURSO

class Entrada_Recurso(TimeStampedModel):
	
	usuario_registra = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='usuario_registra' , blank=True, null=True)
	solicitud_recurso = models.ForeignKey(Solicitud_Recurso , on_delete=models.DO_NOTHING, blank=True, null=True)
	nro_doc = models.CharField(max_length=50,blank=True, null=True)
	detalle = models.CharField(max_length=250,blank=True, null=True)
	nuevo_bien = models.ForeignKey(Bien, blank=True, null=True)	
	conforme = models.BooleanField(choices=BOOL_CHOICES, default=True)
	observacion = models.CharField(max_length=250, blank=True, null=True)

	# DE SER NECESARIO AGREGAR AQUI QUE EQUIPO ENTRA Y POR CUAL SE REEMPLAZA 

	class Meta:
		verbose_name = "Entrada de Recurso"
		verbose_name_plural = "Entrada de Recursos"
		db_table = "Entrada_Recurso"
	def __unicode__(self):
		return '%s' % (self.detalle)



class Diagnostico_Inicial(TimeStampedModel):	
	tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='tecnico',blank=True,null=True)
	diagnostico = models.CharField(max_length=250)
	incidencia = models.ForeignKey(Incidencia , on_delete=models.DO_NOTHING, blank=True,null=True)	
	bienes_recibidos = models.ManyToManyField(Bien, blank=True,through= 'Diagnostico_Bien')	

	class Meta:
		verbose_name = "Diagnostico Inicial"
		verbose_name_plural = "Diagnosticos Inicial"
		db_table = "Diagnostico_Inicial"
	def __unicode__(self):
		return '%s' % (self.diagnostico)



class Diagnostico_Bien(TimeStampedModel):	
	bien = models.ForeignKey(Bien, on_delete=models.DO_NOTHING)
	diagnostico = models.ForeignKey(Diagnostico_Inicial, on_delete=models.DO_NOTHING)
	recibido = models.BooleanField(default=False)
	verificado = models.BooleanField(default=False)

	class Meta:
		verbose_name = "Diagnostico_Bien"
		verbose_name_plural = "Diagnostico_Bienes"
		db_table = "Diagnostico_Bien"
	def __unicode__(self):
		return '%s - %s' % (self.bien, self.diagnostico)
