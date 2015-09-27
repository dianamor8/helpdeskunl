# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from helpdeskunl.apps.centro_asistencia.models import *
from helpdeskunl.apps.usuarios.models import *
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.problema.models import *
from helpdeskunl.apps.accion.models import *

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

class Cambio(TimeStampedModel):
	titulo = models.CharField(max_length=100, verbose_name='Titulo')	
	problema = models.ForeignKey("problema.Problema", on_delete=models.DO_NOTHING, blank=True, null=True)		
	recurso_asignado = models.BooleanField(default=False) #CUANDO SE REGISTRA LA ENTRADA DEL EQUIPO PONER TRUE Y SINO PONER FALSE Y RETORNAR EL PROBLEMA PARA QUE SE SOLUCIONE COMO SEA O SE CIERRE

	class Meta:
		verbose_name = "Cambio"
		verbose_name_plural = "Cambios"
		db_table = "Cambio"
	def __unicode__(self):
		return '%s - %s'%(self.titulo, self.problema)