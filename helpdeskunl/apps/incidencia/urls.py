
from django.conf.urls import patterns, url

urlpatterns = patterns('helpdeskunl.apps.incidencia',	
	#APP INCIDENCIA->DEPENDENCIA
	url(r'^add/dependencia/$', 'views.add_dependencia_view',name = 'view_add_dependencia'),		
)