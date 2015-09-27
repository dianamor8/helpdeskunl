from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings  
from django.utils.functional import curry
from django.views.defaults import *

if settings.DEBUG:
	urlpatterns = patterns('',
	    # Examples:
	    # url(r'^$', 'heladmin.autodiscover()pdeskunl.views.home', name='home'),
	    # url(r'^blog/', include('blog.urls')),
		url(r'^admin/', include(admin.site.urls)),
		url(r'^', include('helpdeskunl.apps.home.urls')),
		url(r'^', include('helpdeskunl.apps.incidencia.urls')),
		url(r'^', include('helpdeskunl.apps.centro_asistencia.urls')),
		url(r'^', include('helpdeskunl.apps.usuarios.urls')),
		url(r'^', include('helpdeskunl.apps.accion.urls')),
		url(r'^', include('helpdeskunl.apps.cambio.urls')),
		url(r'^', include('helpdeskunl.apps.problema.urls')),
		url(r'^', include('helpdeskunl.apps.base_conocimiento.urls')),
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),		
	)
handler500 = curry(server_error, template_name='500.html')
handler404 = curry(page_not_found, template_name='404.html')
handler403 = curry(permission_denied, template_name='403.html')
# handler400 = 'helpdeskunl.views.handler400'
# handler403 = 'helpdeskunl.views.handler403'
# handler404 = 'helpdeskunl.views.handler404'
# handler500 = 'helpdeskunl.views.handler500'

