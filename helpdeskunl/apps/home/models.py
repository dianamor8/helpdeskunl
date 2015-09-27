# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from helpdeskunl.apps.home.current_user import get_current_user
from django.core.urlresolvers import reverse

from drealtime import iShoutClient
ishout_client = iShoutClient()

class TimeStampedModel(models.Model):
	creado_en = models.DateTimeField(auto_now_add=True)
	actualizado_en = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)
	creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_requests_created', default=get_current_user)
	
	class Meta:
		abstract = True


NUEVA_INCIDENCIA='0'
ASIGNAR_INCIDENCIA='1'
REDIRIGIR_INCIDENCIA='2'
ELIMINAR_ASIGNACION_INCIDENCIA='3'
REDIRIGIR_INCIDENCIA_USUARIOS='4'
NOTIFICACIONES_CHOICES = (
	(NUEVA_INCIDENCIA, 'Nueva Incidencia.'),
	(ASIGNAR_INCIDENCIA, 'Asignación de Incidencia'),
	(REDIRIGIR_INCIDENCIA, 'Incidencia Redirigida'),
	(ELIMINAR_ASIGNACION_INCIDENCIA, 'Asignación de Incidencia'),
	(REDIRIGIR_INCIDENCIA, 'Incidencia Redirigida'),
)


class Notificacion(TimeStampedModel):

	destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='destinatario')
	remitente = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='remitente')
	mensaje = models.CharField(max_length=250)
	visto = models.BooleanField(default=False)
	tipo = models.CharField(choices=NOTIFICACIONES_CHOICES, max_length=10)
	fecha = models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name = "Notificación"
		verbose_name_plural = "Notificaciones" 
		db_table = ('Notificacion') 

	def construir_notificacion(self, extra="", ruta=""):
		mensaje = ""

		if self.tipo == '0': #NUEVA INCIDENCIA
			mensaje = "Nueva entrada en el centro %s" % (extra) 
		
		if self.tipo == '1': #ASIGNACIÓN INCIDENCIA
			mensaje = "%s te ha asignado la solución a una incidencia" % (self.remitente) 

		if self.tipo == '2': #REDIRIGIR INCIDENCIA
			mensaje = "%s ha redigido una incidencia a este centro" % (self.remitente) 

		if self.tipo == '3': #ELIMINAR ASIGNACIÓN INCIDENCIA
			mensaje = "La incidencia %s te ha sido removida. Otro asesor ha sido asignado" % (extra) #ENVIAR EN EXTRA EL NUMERO DE INCIDENCIA Y TITULO

		if self.tipo == '4': #REDIRIGIR INCIDENCIA USUARIOS
			mensaje = "La incidencia %s te ha sido removida. Ha sido redirigida a otro centro" % (extra) 

		self.mensaje = mensaje
		self.save()		
		
	def notificar(self):
		ishout_client.emit(self.destinatario.id, 'notificaciones', data = {'msg': self.mensaje, 'tipo':self.get_tipo_display()})
	
	def __unicode__(self):
		return self.mensaje


class Contacto(TimeStampedModel):
	nombres = models.CharField(max_length=120)
	departamento = models.CharField(max_length=120)
	correo = models.EmailField(verbose_name='Dirección de correo',max_length=255,unique=True)
	telefono = models.CharField(max_length=20)
	
	class Meta:
			verbose_name = "Contacto"
			verbose_name_plural = "Contactos"
			db_table = "Contacto"
	
	def __unicode__(self):
		return '%s - %s'%(self.departamento, self.nombres)



# PARA INSTALACION DE HERRAMIENTAS REALTIME DOCUMENTACIÓN
# https://github.com/anishmenon/django-realtime
# https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-an-ubuntu-14-04-server
# http://html5facil.com/tutoriales/como-instalar-node-js-y-socket-io-en-ubuntu/
# https://bitbucket.org/inzane/ishout/src
# https://www.youtube.com/watch?t=779&v=OEOU6TtZEa0
# http://www.webbizarro.com/aplicaciones/1394/agrega-notificaciones-en-tiempo-real-a-tus-sitios/
# https://pythonbc.com/blog/usando-redis-como-manejador-de-cache-y-sesiones-en-django/
# http://michal.karzynski.pl/blog/2013/07/14/using-redis-as-django-session-store-and-cache-backend/
# https://github.com/lovell/sharp/issues/163
# http://www.cuelogic.com/blog/how-to-use-both-django-nodejs-as-backend-for-your-application/
# http://davidnoelte.tumblr.com/post/18788568321/django-with-nodejs-and-socketio
# http://www.maxburstein.com/blog/realtime-django-using-nodejs-and-socketio/
# http://www.jqueryrain.com/?BPS53Amk

