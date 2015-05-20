# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from helpdeskunl.apps.centro_asistencia.models import *

class form_agregar_centro_asistencia(ModelForm):	
	class Meta:
		model = Centro_Asistencia
		labels = {
			'nombre': ('Nombre:'),
			'descripcion': ('Descripción:'),
			'administrador':('Usuario Administrador:'),
		}
		error_messages = {
			'nombre': {'required': u"Este valor no puede estar vacío.",},
			'descripcion': {'required': u"Este valor no puede estar vacío.",},
			'administrador': {'required': u"Seleccione un usuario.",},
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de Centro De Asistencia.',}),			
			'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descripción del Centro de Asistencia.',}),				
			'administrador': forms.Select(attrs={'class':'form-control required'}),
		}