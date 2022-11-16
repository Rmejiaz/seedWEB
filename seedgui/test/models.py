from django.db import models



class Image(models.Model):
    title = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='pics')
    fecha = models.DateField()
    



# Create your models here.
