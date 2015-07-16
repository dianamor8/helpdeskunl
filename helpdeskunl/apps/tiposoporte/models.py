from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
# Create your models here.


class Centro(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=250)	
	usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Operativo')
	class Meta:
		verbose_name = "Centro"
		verbose_name_plural = "Centros"
		db_table = 'Centro'

class Operativo(models.Model):
    centro = models.ForeignKey(Centro)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)    
    tipo_usuario = models.CharField(max_length=64)
    grupo = models.ForeignKey(Group)
    