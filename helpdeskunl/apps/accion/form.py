# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.problema.models import *
from helpdeskunl.apps.cambio.models import *
from helpdeskunl.apps.centro_asistencia.models import *
from helpdeskunl.apps.usuarios.models import *
from helpdeskunl.apps.accion.models import *
from django.forms.models import inlineformset_factory
from helpdeskunl.apps.home.my_wiget import MultiSelectWidget 
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode, force_text
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy
from django.db.models import Q

class Diagnostico_InicialForm(forms.ModelForm):	
	class Meta:
		model = Diagnostico_Inicial
		fields = ('diagnostico',)
		labels = {			
			'diagnostico': ('Diagnostico:'),			
		}
		error_messages = {			
			'diagnostico': {'required': u"Este campo no puede estar vacío",},
		}
		widgets = {
			'diagnostico': forms.Textarea(attrs={'class':'form-control expandable' ,'placeholder':'Diagnostico inicial de la incidencia.',}),
		}

class AccionForm(forms.ModelForm):	
	class Meta:
		model = Accion
		fields = ('titulo', 'descripcion','visible_usuario',)
		labels = {			
			'titulo': ('Título:'),			
			'descripcion': ('Descripcion:'),
			'visible_usuario': ('Visible al solicitante:'),			
		}
		error_messages = {			
			'titulo': {'required': u"Este campo no puede estar vacío",},
			'descripcion': {'required': u"Este campo no puede estar vacío",},
		}
		widgets = {
			'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Título de la acción.',}),			
			'descripcion': forms.Textarea(attrs={'class':'form-control expandable' ,'placeholder':'Describa la acción realizada.',}),
			'visible_usuario': forms.CheckboxInput(attrs={'class':''}),			
		}


class Solicitud_RecursoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		my_user = kwargs.pop('my_user')
		super(Solicitud_RecursoForm, self).__init__(*args, **kwargs)
		self.fields['proveedor']=forms.ModelChoiceField(empty_label='>> SELECCIONE <<', queryset=Contacto.objects.filter(Q(tipo='1')|Q(perfil=my_user)), widget=forms.Select(attrs={'class':'form-control'}))
		self.fields['proveedor'].error_messages = {'required': 'Seleccione quien proveerá el recurso.'}
		self.fields['tipo'].empty_label = ">> SELECCIONE <<"		

	class Meta:
		model = Solicitud_Recurso
		fields = ('recurso', 'proveedor', 'tipo', 'esperar', 'notificar_email')
		widgets = {
			'proveedor': forms.Select(attrs={'class':'form-control required'}),
			'recurso': forms.Textarea(attrs={'class':'form-control' ,'placeholder':'Describa el recurso que desea solicitar.',}),
			'tipo': forms.Select(attrs={'class':'form-control required'}),	
			'esperar': forms.RadioSelect,
			'notificar_email': forms.RadioSelect,			
		}
		labels = {			
			'proveedor': ('Proveedor:'),			
			'recurso': ('Recurso:'),			
			'tipo': ('Tipo:'),
			'esperar': ('¿Dejar la incidencia en espera del recurso?:'),
			'notificar_email': ('Notificar por email:'),
			# 'visible_usuario': ('Visible al solicitante:'),			
		}
		error_messages = {
			'proveedor': {'required': u"Seleccione una opción.",},
			'recurso': {'required': u"Este campo no puede estar vacío.",},
			'tipo': {'required': u"Seleccione una opción.",},			
		}
		

class Entrada_RecursoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):	
		super(Entrada_RecursoForm, self).__init__(*args, **kwargs)
		# self.fields['nro_doc'].widget = forms.HiddenInput(attrs={'id':'Input_nro_doc','class':'form-control', 'placeholder':'Número de oficio, referencia de factura, u otro.',})
		# self.fields['detalle'].widget = forms.HiddenInput(attrs={'id':'Input_detalle','class':'form-control', 'placeholder':'Describa el recurso a recibir.',})
		# self.fields['observacion'].widget = forms.HiddenInput(attrs={'id':'Input_observacion','class':'form-control', 'placeholder':'Describa el motivo por el que no se han asignado los recursos.',})

	class Meta:
		model = Entrada_Recurso
		fields = ('conforme','nro_doc', 'detalle', 'observacion')
		widgets = {
			'nro_doc': forms.TextInput(attrs={'id':'Input_nro_doc','class':'form-control', 'placeholder':'Número de oficio, referencia de factura, u otro.',}),			
			'detalle': forms.Textarea(attrs={'id':'Input_detalle','class':'form-control expandable' ,'placeholder':'Describa el recurso a recibir.',}),		
			'conforme': forms.RadioSelect,	
			'observacion': forms.Textarea(attrs={'id':'Input_observacion','class':'form-control expandable' ,'placeholder':'Describa el motivo por el que no se han asignado los recursos.',}),		
		}
		labels = {			
			'nro_doc': ('Nro. Doc.:'),			
			'detalle': ('Detalle:'),
			'conforme': ('¿Se ha asignado el recurso solicitado?:'),						
			'observacion': ('Observación:'),
		}		

class Entrada_Recurso_EditForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):	
		super(Entrada_Recurso_EditForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Entrada_Recurso
		fields = ('nro_doc', 'detalle', 'observacion')
		widgets = {
			'nro_doc': forms.TextInput(attrs={'id':'Input_nro_doc','class':'form-control', 'placeholder':'Número de oficio, referencia de factura, u otro.',}),			
			'detalle': forms.Textarea(attrs={'id':'Input_detalle','class':'form-control expandable' ,'placeholder':'Describa el recurso a recibir.',}),					
			'observacion': forms.Textarea(attrs={'id':'Input_observacion','class':'form-control expandable' ,'placeholder':'Describa el motivo por el que no se han asignado los recursos.',}),		
		}
		labels = {			
			'nro_doc': ('Nro. Doc.:'),			
			'detalle': ('Detalle:'),
			'observacion': ('Observación:'),
		}		


		

