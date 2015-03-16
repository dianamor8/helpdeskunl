# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from helpdeskunl.apps.incidencia.form import *
from helpdeskunl.apps.incidencia.models import *

# Create your views here.

def add_dependencia_view(request):
	if request.method == 'POST':
		form_dependencia = Dependencia_Form(request.POST)
		if form_dependencia.is_valid():			
			dependencia = form_dependencia.save()
			mensaje = 'Información guardada satisfactoriamente.'
			form_dependencia = Dependencia_Form()			
		else:
			mensaje = 'La información contiene datos incorrectos.'
		ctx = {'form':form_dependencia, 'mensaje':mensaje}
		return render (request, 'incidencia/dependencia/add_dependencia.html', ctx)
	else:		
		mensaje = 'Nueva dependencia'
		form_dependencia = Dependencia_Form()	
		ctx = {'form':form_dependencia, 'mensaje':mensaje}		
		return render (request, 'incidencia/dependencia/add_dependencia.html', ctx)
