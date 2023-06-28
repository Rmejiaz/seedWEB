from celery import shared_task
from .models import Experimento
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Image
from .models import Semillas
from .models import Mask
from datetime import datetime, timedelta
from django.utils import timezone
from .camera import VideoCamera
import time
from django.contrib.admin.views.decorators import staff_member_required
import cv2
import plotly.express as px
import pandas as pd
from plotly.offline import plot
import io
from .counter import Counter

from celery import Celery
from time import strftime
import time
from .control_camera import MoverCamara
from seedgui.celery import app

def move_camera(pos): # Luego se reemplaza por la función que mueve la camara.
    time.sleep(2)
    print(f"Camara en bandeja {pos}")
    
def home_camera(): # Luego se reemplaza por la función que mueve la camara.
    time.sleep(2)
    print(f"Camara en home")

def light_on(): # Luego se reemplaza por la función que prende el led
    print("Led prendido")

def light_off(): # Luego se reemplaza por la función que apaga el led
    print("Led apagado")

@shared_task(bind=True)
def captura(self, experimento_id):
    # Do a capture for a given experiment

    print("Capturando!")
    experimento = get_object_or_404(Experimento, pk = experimento_id)

    # Here goes the logic for the camera movement to the specific petri dish

    bandeja = experimento.dish.number
    
    control = MoverCamara() # Instanciar controlador de movimiento
    control.home() # Mover la camara al home
    control.led_on() # Prender led
    control.pos_camara(bandeja) # Mover la camara a la posición deseada
    time.sleep(1) # Esperar un segundo para asegurar que la camara si este quieta

   # home_camera()
    #light_on() # Se prende el led
    #move_camera(bandeja) # Se mueve la camara a la respectiva bandeja
    #time.sleep(1) # Esperar un segundo para asegurar que la camara si este quieta

    camera = VideoCamera(Image)
    counter = Counter("./yolov8.tflite")

    fecha = datetime.now()
    fecha_conteo = timezone.now()
    path, image = camera.save_frame(fecha, experimento)
    print("Saved image")
    camera.release() # Liberar la camara para que pueda ser usada en otros experimentos

    # Conteo y guardado de imagen:
    out_path = path.replace("images", "detection")
    
    result, count_ = counter.predict(image)
    print(count_)

    conteo = Semillas(fecha = fecha_conteo, 
                        germinadas = count_['germinated'], 
                        no_germinadas = count_['no_germinated'],
                        experimento = experimento)

    conteo.save()

    experimento.imagenes_capturadas = experimento.imagenes_capturadas + 1
    experimento.progreso = (experimento.imagenes_capturadas/experimento.cantidad_imagenes)*100

    if experimento.progreso >= 100:
        experimento.status = "Finalizado"
        experimento.dish.is_available = True
        cv2.imwrite(out_path, result)
        mask = Mask(mask=out_path, experimento = experimento, fecha = fecha)
        mask.save()
        experimento.save()
        control.home() # Llevar la camara al home
        control.led_off() # Apagar led
        control.release_control() # Liberar pines
        experimento = get_object_or_404(Experimento, pk=experimento_id) 
        experimento.task.delete()
        experimento.save()
    cv2.imwrite(out_path, result)
    mask = Mask(mask = out_path, experimento = experimento, fecha = fecha)
    mask.save()

   
    experimento.save()

    control.home() # Llevar la camara al home
    control.led_off() # Apagar led
    control.release_control() # Liberar el controlador para que pueda ser usado por otros experimentos


    #home_camera() # Se lleva la camara nuevamente al punto de partida
    #light_off() # Se apaga el led
