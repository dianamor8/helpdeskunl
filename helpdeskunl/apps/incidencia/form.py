# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.centro_asistencia.models import *
from helpdeskunl.apps.usuarios.models import *
from django.forms.models import inlineformset_factory
from helpdeskunl.apps.home.my_wiget import MultiSelectWidget 
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode, force_text
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy

class BienForm(ModelForm):
	class Meta:
		model = Bien
		exclude = ('validado', 'tipo', 'padre', 'estado',)
		labels = {
			'codigo': ('Código:'),
			'codigo_cfn': ('Código M.F.:'),
			'producto': ('Artículo/Bien:'),			
		}
		error_messages = {
			'codigo': {'required': u"Este campo no puede estar vacío.",},
			'producto': {'required': u"Este campo no puede estar vacío.",},
		}
		widgets = {
			'codigo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código de bodega del bien institucional.',}),			
			'codigo_cfn': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código asignado por el Ministerio de Finanzas.',}),
			'producto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descripción general del bien.',}),
		}

class Caracteristica_BienForm(ModelForm):
	class Meta:
		model = Caracteristica_Bien
		exclude = ('estado',)
		labels = {
			'tipo': ('Característica:'),
			'detalle': ('Valor:'),			
		}
		widgets = {
			'tipo': forms.Select(attrs={'class':'form-control required'}),
			'detalle': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Caracteristica.',}),
		}
		error_messages = {
			'tipo': {'required': u"Seleccione una opción.",},
			'detalle': {'required': u"Este campo no puede estar vacío.",},			
		}

Caracteristica_BienFormSet = inlineformset_factory(Bien, Caracteristica_Bien, form=Caracteristica_BienForm)

class IncidenciaForm(forms.ModelForm):	

	def __init__(self, *args, **kwargs):		
		my_user = kwargs.pop('my_user')
		super(IncidenciaForm, self).__init__(*args, **kwargs)
		self.fields['centro_asistencia']=forms.ModelChoiceField(empty_label='>> SELECCIONE <<', queryset=Centro_Asistencia.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
		self.fields['centro_asistencia'].error_messages = {'required': 'Seleccione el centro que atenderá su solicitud.'}
		self.fields['justif_urgencia'].widget = forms.HiddenInput(attrs={'id':'Input_urgencia','class':'form-control', 'placeholder':'Justifique su solicitud de urgencia.',})
		## self.fields['bienes'].help_text = 'Seleccione los bienes que desee reportar en esta incidencia.'
		## self.fields['bienes'].queryset = Bien.objects.filter(custodio=my_user)
		self.fields['imagen'].widget=MyClearableFileInput()
		
	class Meta:
		model = Incidencia
		exclude = 'fecha', 'solicitante', 'prioridad_asignada', 'estado_incidencia', 'estado', 'creado_por', 'nivel', 'tecnicos','servicio', 'ejecucion', 'duracion', 'caduca', 'bienes'
		
		widgets = {
			'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Título de solicitud.',}),
			'descripcion': forms.Textarea(attrs={'class':'form-control expandable' ,'placeholder':'Descripción de la solicitud.',}),
			'prioridad_solicitada': forms.Select(attrs={'class':'form-control required'}),			
		}
		labels = {
			'titulo': ('Título:'),
			'descripcion': ('Descripción:'),
			'prioridad_solicitada': ('Prioridad:'),			
			'centro_asistencia': ('Centro de Asistencia:'),
			'justif_urgencia': ('Justifique:'),
		}
		error_messages = {
			'titulo': {'required': u"Este campo no puede estar vacío.",},
			'descripcion': {'required': u"Este campo no puede estar vacío.",},
			'centro_asistencia': {'required': u"Seleccione el centro que atenderá su solicitud.", 'placeholder':'Seleccione.',},
		}

	def clean_justif_urgencia(self):
		data = self.cleaned_data['justif_urgencia']
		data_selected = self.cleaned_data['prioridad_solicitada']
		print data_selected
		if data_selected == '2':
			if not data:
				raise forms.ValidationError("Justifique su selección de urgencia.")
		else:
			data = ''
		return data

my_default_errors = {
    'required': 'Seleccione al menos un valor',
    'invalid': 'El valor seleccionado no es válido'
}
# PARA ACTUALIZAR POR EL ADMIN
class IncidenciaCompleteForm(forms.ModelForm):
		
	def __init__(self, *args, **kwargs):		
		my_user = kwargs.pop('my_user')
		qs = kwargs.pop('perfiles')
		qq = kwargs.pop('servicios')		
		super(IncidenciaCompleteForm, self).__init__(*args, **kwargs)		
		## self.fields['bienes'].help_text = 'Seleccione los bienes que desee reportar en esta incidencia.'
		## self.fields['bienes'].queryset = Bien.objects.filter(custodio=my_user)
		self.fields['tecnicos'].help_text = 'Seleccione los técnicos que atenderán la incidencia.'
		self.fields['tecnicos'].queryset = qs
		self.fields['servicio'].queryset = qq		
		self.fields['servicio'].empty_label = ">>>SELECCIONE<<<"		
		self.fields['duracion'].widget.attrs['readonly'] = True		
		# self.fields['caduca'].widget.format = '%d/%m/%Y'


		
	class Meta:
		model = Incidencia
		fields = 'nivel',  'prioridad_asignada',  'servicio','duracion', 'tecnicos',
		
		widgets = {			
			'prioridad_solicitada': forms.Select(attrs={'class':'form-control', 'id':'p_solicitada',}),			
			'prioridad_asignada': forms.Select(attrs={'class':'form-control', 'id':'p_asignada',}),
			'nivel': forms.Select(attrs={'class':'form-control',}),
			'servicio': forms.Select(attrs={'class':'form-control', 'id':'sla',}),		#MOSTRAR SOLO LOS SERVICIOS DEL CENTRO QUE ESCOJA				
			'duracion': forms.TextInput(attrs={'class':'form-control', 'id':'duracion',}),
		}
		labels = {			
			'prioridad_solicitada': ('Prioridad Solicitada:'),			
			'prioridad_asignada': ('Prioridad Asignada:'),
			'nivel': ('Nivel de Incidencia:'),
			'servicio': ('Servicio. SLA.:'),
			'duracion': ('Duración:'),
			# 'bienes': ('Bienes:'),
			'tecnicos': ('Asesores Técnicos:'),
		}
		error_messages = {
			'prioridad_solicitada': {'required': u"Seleccione una opción.",},
			'prioridad_asignada': {'required': u"Seleccione una opción.",},			
			'nivel': {'required': u"Seleccione una opción.",},
			'servicio': {'required': u"Seleccione una opción.",},
			'tecnicos': {'required': u"Seleccione al menos una opción.",},	
		}	



class AsignacionForm(forms.ModelForm):	

	tecnicos = forms.ModelMultipleChoiceField(queryset=Perfil.objects.none(), required=True, error_messages=my_default_errors)	
	
	def __init__(self, *args, **kwargs):
		qs = kwargs.pop('perfiles')
		qq = kwargs.pop('servicios')
		super(AsignacionForm, self).__init__(*args, **kwargs)
		self.fields['tecnicos'].queryset = qs
		self.fields['servicio'].queryset = qq		
		self.fields['servicio'].empty_label = ">>>SELECCIONE<<<"		

	class Meta:
		model = Incidencia
		fields = 'prioridad_asignada','servicio',
		widgets = {		
			'prioridad_asignada': forms.Select(attrs={'class':'form-control required'}),	
			'servicio': forms.Select(attrs={'class':'form-control required'}),			
		}	
		labels = {
			'tecnicos': ('Técnicos:'),
			'prioridad_asignada': ('Asignar Prioridad:'),
			'servicio': ('Acuerdo de nivel de servicio:'),
		}
		error_messages = {
			'tecnicos': {'required': u"Seleccione al menos un valor.",},
			'prioridad_asignada': {'required': u"Seleccione una opción.",},			
			'servicio': {'required': u"Seleccione una opción.",},	
		}

	def clean_servicio(self):
		data = self.cleaned_data['servicio']		
		if data is None:			
			raise forms.ValidationError("Asigne un servicio a la incidencia.")	
		return data


class RedirigirIncidenciaForm(forms.ModelForm):	

	def __init__(self, *args, **kwargs):
		centro_asistencia = kwargs.pop('centro_asistencia')
		super(RedirigirIncidenciaForm, self).__init__(*args, **kwargs)		
		self.fields['centro_asistencia']=forms.ModelChoiceField(label ='Centro de Asistencia', empty_label='>> SELECCIONE <<', queryset=Centro_Asistencia.objects.exclude(id=centro_asistencia.id), widget=forms.Select(attrs={'class':'form-control'}))
		self.fields['centro_asistencia'].error_messages = {'required': 'Redirija el centro que atenderá la solicitud.'}
		
	class Meta:
		model = Incidencia
		fields = ('centro_asistencia',)

		labels = {			
			'centro_asistencia': ('Centro de Asistencia:'),			
		}
		error_messages = {			
			'centro_asistencia': {'required': u"Seleccione el centro que atenderá su solicitud.", 'placeholder':'Seleccione.',},
		}
		


class MyClearableFileInput(ClearableFileInput):

	initial_text = ugettext_lazy('Actualmente')
	input_text = ugettext_lazy('Cambiar')
	clear_checkbox_label = ugettext_lazy('Borrar')
	template_with_initial = '%(initial_text)s: %(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
	template_with_clear = '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'
	url_markup_template = '<a href="{0}">{1}</a>'
	
	def render(self, name, value, attrs=None):
		substitutions = {
			'initial_text': self.initial_text,
			'input_text': self.input_text,
			'clear_template': '',
			'clear_checkbox_label': self.clear_checkbox_label,
		}

		template = '%(input)s'
		substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

		if value and hasattr(value, "url"):
			template = self.template_with_initial
			substitutions['initial'] = format_html(self.url_markup_template,value.url,force_text(value))
			if not self.is_required:
				checkbox_name = self.clear_checkbox_name(name)
				checkbox_id = self.clear_checkbox_id(checkbox_name)
				substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
				substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
				substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
				substitutions['clear_template'] = self.template_with_clear % substitutions
		return mark_safe(template % substitutions)

# HIDDEN FORM POR CONDICION
# http://solvedstack.com/questions/change-a-django-form-field-to-a-hidden-field

