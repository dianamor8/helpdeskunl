
from django.conf.urls import patterns, url
from helpdeskunl.apps.incidencia.views import * 

urlpatterns = patterns('helpdeskunl.apps.incidencia',	
	#APP INCIDENCIA->DEPENDENCIA
	# url(r'^add/dependencia/$', 'views.add_dependencia_view',name = 'view_add_dependencia'),
	# INCIDENCIA	
	url(r'^incidencia/add$', IncidenciaCreate.as_view(), name='incidencia_add'),
	url(r'^incidencia/list$', IncidenciaList.as_view(), name='incidencia_list'),
	url(r'^incidencia/asignada/list$', Incidencia_AsignadaList.as_view(), name='incidencia_asignada_list'),
	url(r'^incidencia/centro/list$', Incidencia_CentroList.as_view(), name='incidencia_centro_list'),
	url(r'^incidencia/edit/(?P<pk>\d+)/$', IncidenciaUpdate.as_view(), name='incidencia_update'),
	url(r'^incidencia/detail/(?P<pk>[-\w]+)/$', Incidencia_DetailView.as_view(), name='incidencia_detail'),
	url(r'^incidencia/(?P<pk>\d+)/delete/$', IncidenciaDelete.as_view(), name='incidencia_delete'),
	url(r'^incidencia/asignacion/(?P<pk>\d+)/$', AsignarIncidencia.as_view(), name='asignarincidencia_update'),
	url(r'^incidencia/redirigir/(?P<pk>\d+)/$', RedirigirIncidencia.as_view(), name='redirigirincidencia_update'),
	url(r'^incidencia/edit/admin/(?P<pk>\d+)/$', IncidenciaCompleteUpdate.as_view(), name='incidencia_complete_update'),
	url(r'^bien/add$', BienCreate.as_view(), name='bien_add'),	
	url(r'^incidencia/atencion/(?P<pk>\d+)/$', Atender_Incidencia_Update.as_view(), name='atender_incidencia'),

	#AJAX
	url(r'^calcularincidencia/$', 'rest.calcular_incidencia_ajax', name='calcularincidencia'),	
	url(r'^bien/busqueda/$', 'rest.buscar_bienes', name='view_buscar_bienes'), 

	

)