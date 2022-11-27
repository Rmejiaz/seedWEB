from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Experimento
from .models import Image
from datetime import datetime, timedelta
from django.utils import timezone
from .camera import VideoCamera
import time
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

@staff_member_required
def index(request):
    return render(request, "experimentos/index.html")

@staff_member_required
def lista_experimentos(request):

    data = Experimento.objects.all()
    context = {'experimentos':data}

    return render(request, 'experimentos/lista_experimentos.html', context)

@staff_member_required
def ver_experimento(request, experimento_id):
    
    experimento = get_object_or_404(Experimento, pk = experimento_id)


    context = {'experimento':experimento}

    return render(request, 'experimentos/detalle.html', context)

@staff_member_required
def iniciar_experimento(request, experimento_id):

    experimento = get_object_or_404(Experimento, pk = experimento_id)

    # Se fija la fecha de inicio:
    experimento.fecha_inicio =  timezone.now()

    # Se cambia el status del experimento:
    experimento.status = 'Iniciado'

    # Se calcula la cantidad de imagenes de acuerdo a la frecuencia y la diferencia entre las fechas:

    tiempo_total = (experimento.fecha_final - experimento.fecha_inicio).total_seconds()/3600 # Tener la duracion en horas
    total_imgs = int(tiempo_total/experimento.frecuencia)

    # Guardar la cantidad de imagenes que se van a capturar:
    experimento.cantidad_imagenes = total_imgs

    experimento.save()


    # Se hacen las capturas (por ahora con un ciclo, preferible hacerlo a nivel del sistema):

    camera = VideoCamera(Image)
    for i in range(total_imgs):
        fecha = datetime.now()
        camera.save_frame(fecha, experimento)
        print("Saved image")
        time.sleep(experimento.frecuencia*3600)

        progreso = ((i+1)/total_imgs)*100
        experimento.progreso = progreso
        experimento.save()
    
    # Cuando termina el for, es porque el experimento termino (falta hacer la segmentacion y el conteo)

    experimento.status = 'Finalizado'
    experimento.save()

    return HttpResponse("Experimento terminado.")

@staff_member_required
def mostrar_resultados(request, experimento_id):

    experimento = get_object_or_404(Experimento, pk = experimento_id)

    images = Image.objects.filter(experimento=experimento)


    context = {'experimento': experimento, 'images':images}

    return render(request, 'experimentos/resultados.html', context)







    



