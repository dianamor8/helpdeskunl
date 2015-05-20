from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from helpdeskunl.settings import LOGIN_URL

# Create your views here.
@login_required
def lista_centro_asistencia(request):
	return render(request, 'centro_asistencia/lista_centro_asistencia.html')