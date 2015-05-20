from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'helpdeskunl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('helpdeskunl.apps.home.urls')),
	url(r'^', include('helpdeskunl.apps.incidencia.urls')),
	url(r'^', include('helpdeskunl.apps.centro_asistencia.urls')),
	url(r'^', include('helpdeskunl.apps.usuarios.urls')),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
	#url(r'^', include(helpdeskunl.apps.tiposoporte.urls)),
)
