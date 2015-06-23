from django.db import models
from helpdeskunl.apps.centro_asistencia.models import *

class Centro_Asistencia_Manager(models.Manager):
	# REQUIERE UN USUARIO PARA LOS CENTROS DE ASISTENCIA ASIGNADOS A UN USUARIO
	def asignado_para_mi(self, user):
		return self.model.objects.filter(usuarios__dni=user)

	def administrado_por_mi(self, user):
		return self.model.objects.filter(usuarios__dni=user, usuarios__groups__name='JEFE DEPARTAMENTO')
		# return self.model.objects.filter(usuarios__dni=user)
		# return super(Centro_Asistencia_Manager, self).get_query_set().filter(creator=user)

# class PersonaManager(models.Manager):

# 	def padre(self):
# 		return self.model.objects.filter(sexo='m').exclude(profesion='Sacerdote')

# 	def get_queryset(self):
#         return super(Centro_Asistencia_Manager, self).get_queryset().filter(author='Roald Dahl')

# EJEMPLO DE MANAGER
 # class UserContactManager(models.Manager): 
 # 	def for_user(self, user): 
 # 		return super(UserContactManager, self).get_query_set().filter(creator=user) 
 # class UserContact(models.Model): [...] objects = UserContactManager()
 
 # contacts = Contact.objects.for_user(request.user)