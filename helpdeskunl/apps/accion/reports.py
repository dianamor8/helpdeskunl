from xhtml2pdf import pisa 
import cStringIO as StringIO 
from django.template.loader import get_template 
from django.template import Context 
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.conf import settings
import os
from helpdeskunl.apps.accion.models import *

# def reporte_solicitud_recurso(request, id_solicitud): 
# 	tipo=id_solicitud
# 	solicitud = Solicitud_Recurso.objects.get(pk = int(tipo))
# 	# template = get_template("accion/reportes/solicitud_recurso.html") 
# 	# context = Context({'pagesize':'A4', 'incidencia':tipo, 'solicitud':solicitud}) 
# 	# html = template.render(context) 
# 	# result = StringIO.StringIO() 
# 	# pdf = pisa.pisaDocument(StringIO.StringIO(html), dest=result, encoding='utf-8') 
# 	outputFilename = "reportes/solicitud_recurso_%s.pdf" %(solicitud.id)
# 	resultFile = open(os.path.join(settings.MEDIA_ROOT, outputFilename), 'r')	
# 	print resultFile

# 	return HttpResponse(resultFile, content_type='application/pdf') 	

# def pdf_view(request):


# AGREGAR USUARIOS LOGEADOS
def reporte_solicitud_recurso(request, id_solicitud):
	try:
		tipo=id_solicitud
		solicitud = Solicitud_Recurso.objects.get(pk = int(tipo))
		outputFilename = "reportes/solicitud_recurso_%s.pdf" %(solicitud.id)				
		pdf = open(os.path.join(settings.MEDIA_ROOT, outputFilename), 'rb').read()
	except Exception, e:
		print e
	return HttpResponse(pdf, content_type='application/pdf')	

# Utility function

def convertHtmlToPdf(id_solicitud):
	# Define your data
	tipo=id_solicitud	
	solicitud = Solicitud_Recurso.objects.get(pk = int(tipo))
	sourceHtml = get_template("accion/reportes/solicitud_recurso.html") 	
	outputFilename = "reportes/solicitud_recurso_%s.pdf" %(id_solicitud)
	context = Context({'pagesize':'A4', 'solicitud':solicitud}) 	
	# open output file for writing (truncated binary)
	resultFile = open(os.path.join(settings.MEDIA_ROOT, outputFilename), "w+b")	
	html= sourceHtml.render(context)
	# convert HTML to PDF
	pisaStatus = pisa.CreatePDF(html.encode("UTF-8"), dest=resultFile, encoding='UTF-8') 
	# resultFile.seek(0)	
	# # close output file
	# pdf = resultFile.read()	
	# resultFile.close()                 # close output file	

	# return True on success and False on errors
	# return pisaStatus.err
	return os.path.join(settings.MEDIA_ROOT, outputFilename)