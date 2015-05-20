from django.conf.urls import patterns, url

urlpatterns = patterns('helpdeskunl.apps.centro_asistencia',	
	#APP INCIDENCIA->DEPENDENCIA
	#url(r'^add/dependencia/$', 'views.add_dependencia_view',name = 'view_add_dependencia'),	
	url(r'^lista/centro_asistencia/$', 'views.lista_centro_asistencia',name = 'view_lista_centro_asistencia'),	
		
)