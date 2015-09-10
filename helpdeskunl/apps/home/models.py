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
NOTIFICACIONES_CHOICES = (
	(NUEVA_INCIDENCIA, 'Nueva Incidencia.'),
	(ASIGNAR_INCIDENCIA, 'Asignación de Incidencia'),
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

	def construir_notificacion(self):
		mensaje = ""

		if self.tipo == '0': #NUEVA INCIDENCIA
			mensaje = "%s ha registrado una nueva incidencia" % (self.remitente) 
		
		if self.tipo == '1': #ASIGNACIÓN INCIDENCIA
			mensaje = "%s te ha asignado la solución a una incidencia" % (self.remitente) 

		self.mensaje = mensaje
		self.save()		
		

	# def notificar_test(remitente, destinatarios, tipo):		
	# 	for destinatario in destinatarios:			
	# 		notificacion = Notificacion(remitente=remitente, destinatario = destinatario, tipo = tipo)
	# 		notificacion.save()			
	# 		notificacion.mensaje = construir_notificacion(notificacion)
	# 		notificacion.save()
	# 		ishout_client.emit(destinatario.id, 'notificaciones', data = {'msg': notificacion.mensaje})
	
	def notificar(self):				
		ishout_client.emit(self.destinatario.id, 'notificaciones', data = {'msg': self.mensaje})
	
	def __unicode__(self):
		return self.mensaje


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

