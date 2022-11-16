from django.db import models

# Create your models here.


class Experimento(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
    frecuencia = models.IntegerField()
    cantidad_imagenes = models.IntegerField()
    observaciones = models.CharField(max_length=200)
    cantidad_semillas = models.IntegerField()

class Image(models.Model):
    photo = models.ImageField(upload_to='pics')
    fecha = models.DateField()
    experimento = models.ForeignKey(Experimento, on_delete=models.CASCADE)

class Mask(models.Model):

    mask = models.ImageField(upload_to='masks')
    fecha = models.DateField()
    experimento = models.ForeignKey(Experimento, on_delete=models.CASCADE)

class Semillas(models.Model):
    fecha = models.DateField()
    germinadas = models.IntegerField()
    no_germinadas = models.IntegerField()
    experimento = models.ForeignKey(Experimento, on_delete=models.CASCADE)
