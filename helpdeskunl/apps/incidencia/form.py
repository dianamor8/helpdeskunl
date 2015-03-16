# -*- coding: utf-8 -*-
from django import forms
from helpdeskunl.apps.incidencia.models import *

class Dependencia_Form(forms.ModelForm):
	class Meta:
		model = Dependencia
		fields = '__all__'
		labels ={
			'nombre' : 'Departamento:',
			'detalle' : 'Dedicado a:',
		}
		default_error_messages = {
			'blank': u'Este campo no puede estar vacío.',
			'required': u'Este campo es requerido',
		}