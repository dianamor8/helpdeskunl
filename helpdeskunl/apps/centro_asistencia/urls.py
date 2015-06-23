from django.conf.urls import patterns, url
from helpdeskunl.apps.centro_asistencia.views import * 

urlpatterns = patterns('helpdeskunl.apps.centro_asistencia',	
	#APP INCIDENCIA->DEPENDENCIA
	#url(r'^add/dependencia/$', 'views.add_dependencia_view',name = 'view_add_dependencia'),	
	# VIEW
	url(r'^lista/centro_asistencia/$', 'views.lista_centro_asistencia',name = 'view_lista_centro_asistencia'),	
	# LIST, DETAIL, CREATE, CHANGE, DELETE VIEWS
	url(r'^centro_asistencia/(?P<pk>[-\w]+)/$', Centro_Asistencia_DetailView.as_view(), name='view_centro_asistencia_detail'),
	url(r'servicio/add/$', ServicioCreate.as_view(), name='servicio_add'),
	url(r'^servicio/(?P<pk>\d+)/$', ServicioUpdate.as_view(), name='servicio_update'),
	url(r'servicio/(?P<pk>\d+)/delete/$', ServicioDelete.as_view(), name='servicio_delete'),
	# REST
	url(r'^centro_asistencia/add$', 'rest.centro_asistencia_add_ajax',name = 'view_centro_asistencia_add'),			
)