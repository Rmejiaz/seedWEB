from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Experimento
# Create your views here.


def index(request):
    return render(request, "experimentos/index.html")


def lista_experimentos(request):

    data = Experimento.objects.all()
    context = {'experimentos':data}

    return render(request, 'experimentos/lista_experimentos.html', context)


def ver_experimento(request, experimento_id):
    
    experimento = get_object_or_404(Experimento, pk = experimento_id)

    if experimento.status == 'Creado':
        return HttpResponse("El experimento no ha sido iniciado, en este página se puede iniciar")
    
    elif experimento.status == 'Activo':
        return HttpResponse("El experimento está en curso, en esta página se pueden ver el avance")
    
    elif experimento.status == 'Finalizado':
        return HttpResponse("El experimento ya finalizó, en esta página se pueden ver y descargar los resultados")