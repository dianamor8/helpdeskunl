# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, UserManager, BaseUserManager, PermissionsMixin, Group, Permission
from django.conf import settings

ADMINISTRATIVO='0'
DOCENTE='1'
TIPO_USUARIO_CHOICES = (
	(ADMINISTRATIVO, 'Administrativo'),
	(DOCENTE, 'Docente'),
)

class PerfilUserManager(BaseUserManager):
		
	def create_user(self, dni, password=None):
		if not dni:
			raise ValueError('El usuario requiere de DNI')		
		user = self.model(dni=dni)
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, dni, password):
		user = self.create_user(dni,password=password)
		user.is_admin = True
		user.save(using=self._db)
		return user

# MANAGER PARA USUARIOS DE TIPO 
class Jefe_Departamento_Manager(models.Manager):
	def get_queryset(self):		
		return super(Jefe_Departamento_Manager, self).get_queryset().filter(groups__name='JEFE DEPARTAMENTO')

class Asesor_Tecnico_Manager(models.Manager):
	def get_queryset(self):
		return super(Asesor_Tecnico_Manager, self).get_queryset().filter(groups__name='ASESOR TECNICO')


# Create your models here.
class Perfil(AbstractBaseUser, PermissionsMixin):	
	#usuario = models.OneToOneField(settings.AUTH_USER_MODEL)	
	dni = models.CharField(max_length=50, unique=True, verbose_name='DNI')
	nombres = models.CharField(max_length=250, verbose_name='Nombres')
	apellidos = models.CharField(verbose_name='Apellidos',max_length=250)
	email = models.EmailField(verbose_name='Dirección de correo',max_length=255,unique=True)
	departamento = models.CharField(max_length=350, verbose_name='Departamento')	
	contacto = models.CharField(max_length=50, verbose_name='Contacto')
	tipo = models.CharField(choices=TIPO_USUARIO_CHOICES, max_length=100, verbose_name='Personal')	
	activo = models.BooleanField(default=True, verbose_name='Usuario UNL activo')
	is_active = models.BooleanField(default=True, verbose_name='Usuario activo')
	is_admin = models.BooleanField(default=False, verbose_name='Usuario Administrador')	
	
	objects = PerfilUserManager()
	jefes_departamento = Jefe_Departamento_Manager()
	asesores_tecnicos = Asesor_Tecnico_Manager()

	class Meta:
		verbose_name = "Perfil"
		verbose_name_plural = "Perfiles"
		db_table = 'Perfil'
	
	USERNAME_FIELD = 'dni'	
	
	def get_full_name(self):
		return self.nombres + ' ' + self.apellidos
	def get_short_name(self):
		return self.dni
	def __unicode__(self):
		return self.dni
	# def has_perm(self, perm, obj=None):
	# 	#"Does the user have a specific permission?"
	# 	# Simplest possible answer: Yes, always
	# 	if self.user_permissions.all():
	# 		return True
	# 	else:
	# 		return False
	def has_module_perms(self, app_label):
		#"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True
	@property
	def is_staff(self):
		# "Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

# EJEMPLOS DE AUTH 
#https://gist.github.com/johnjwatson/5442906
#http://procrastinatingdev.com/django/using-configurable-user-models-in-django-1-5/
#https://github.com/django/django/blob/master/django/contrib/auth/models.py#L231
#https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#a-full-example
#http://buildthis.com/customizing-djangos-default-user-model/
#http://www.lasolution.be/blog/creating-custom-user-model-django-16-part-1.html
#https://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/
