from django.db import models

# Create your models here.


class Experimento(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateTimeField(blank=True, editable = False, null = True)
    fecha_final = models.DateTimeField()
    frecuencia = models.FloatField()
    cantidad_imagenes = models.IntegerField(editable = False, null = True)
    imagenes_capturadas = models.IntegerField(editable=False, default=0)
    observaciones = models.CharField(max_length=200)
    cantidad_semillas = models.IntegerField()
    status = models.CharField(max_length=20, default = "Creado", editable = False)
    progreso = models.FloatField(default = 0, editable = False)

class Image(models.Model):
    photo = models.ImageField(upload_to='pics')
    fecha = models.DateTimeField()
    experimento = models.ForeignKey(Experimento, on_delete=models.CASCADE)

class Mask(models.Model):

    mask = models.ImageField(upload_to='masks')
    fecha = models.DateTimeField()
    experimento = models.ForeignKey(Experimento, on_delete=models.CASCADE)

class Semillas(models.Model):
    fecha = models.DateTimeField()
    germinadas = models.IntegerField()
    no_germinadas = models.IntegerField()
    experimento = models.ForeignKey(Experimento, on_delete=models.CASCADE)
