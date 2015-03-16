from django.contrib import admin

# Register your models here.
from helpdeskunl.apps.incidencia.models import *

admin.site.register(Incidencia)
admin.site.register(Dependencia)
admin.site.register(Categoria_Equipo)
admin.site.register(Marca_Equipo)
admin.site.register(Equipo)
admin.site.register(Codigo_Bodega)
admin.site.register(Detalle_Equipos)
