from django.db import models
from helpdeskunl.apps.centro_asistencia.models import *

class Centro_Asistencia_Manager(models.Manager):
	def get_queryset(self):
		return super(Centro_Asistencia_Manager, self).get_queryset().filter(estado=True)

	# REQUIERE UN USUARIO PARA LOS CENTROS DE ASISTENCIA ASIGNADOS A UN USUARIO
	def asignado_para_mi(self, user):
		####->return self.model.objects.filter(usuarios__dni=user)
		return self.model.objects.filter(estado=True, personal_operativo__usuario__dni=user).exclude(personal_operativo__grupo__name='JEFE DEPARTAMENTO')

	def administrado_por_mi(self, user):
		######->return self.model.objects.filter(usuarios__dni=user, usuarios__groups__name='JEFE DEPARTAMENTO')
		return self.model.objects.filter(estado=True, personal_operativo__usuario__dni=user, personal_operativo__grupo__name='JEFE DEPARTAMENTO')
		# return self.model.objects.filter(usuarios__dni=user)
		# return super(Centro_Asistencia_Manager, self).get_query_set().filter(creator=user)

	def centro_administrado_por_mi(self, user, centro):
		###->return self.model.objects.filter(usuarios__dni=user, usuarios__groups__name='JEFE DEPARTAMENTO', pk=centro)
		return self.model.objects.filter(estado=True, personal_operativo__usuario__dni=user, personal_operativo__grupo__name='JEFE DEPARTAMENTO', pk=centro)

	def acesorado_por_mi(self, user):		
		return self.model.objects.filter(estado=True, personal_operativo__usuario__dni=user, personal_operativo__grupo__name='ASESOR TECNICO')
	

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