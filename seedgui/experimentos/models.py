from django.db import models

# Create your models here.

import json
from django.db import models
from django.utils import timezone
from django_enum_choices.fields import EnumChoiceField
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from .enums import TimeInterval, SetupStatus
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

# class Setup(models.Model):
#     class Meta:
#         verbose_name = 'Setup'
#         verbose_name_plural = 'Setups'
#     title = models.CharField(max_length=70, blank=False)
#     status = EnumChoiceField(SetupStatus, default=SetupStatus.active)
#     created_at = models.DateTimeField(auto_now_add=True)
#     time_interval = EnumChoiceField(
#         TimeInterval, default=TimeInterval.five_mins)
#     task = models.OneToOneField(
#         PeriodicTask,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True
#     )

class PetriDish(models.Model):
    number = models.PositiveIntegerField(unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        # f"Petri Dish {self.number} - {}"
        return f"Petri Dish {self.number} - {'Disponible' if self.is_available else 'No Disponible'}"
        
    class Meta:
        verbose_name = f"Petri Dish"
        verbose_name_plural = "Petri Dishes"

class Experimento(models.Model):
    class Meta:
        verbose_name = 'Experimento'
        verbose_name_plural = 'Experimentos'
    nombre = models.CharField(max_length=50, blank=False)
    dish = models.ForeignKey(PetriDish, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(blank=True, editable = False, null = True)
    fecha_final = models.DateTimeField()
    cantidad_imagenes = models.IntegerField(editable = False, null = True)
    imagenes_capturadas = models.IntegerField(editable=False, default=0)
    observaciones = models.TextField(max_length=200)
    status = models.CharField(max_length=20, default = "Iniciado", editable = False)
    progreso = models.FloatField(default = 0, editable = False)

    status_2 = EnumChoiceField(SetupStatus, default=SetupStatus.activo, editable = False)
    created_at = models.DateTimeField(auto_now_add=True)
    time_interval = EnumChoiceField(
        TimeInterval, default=TimeInterval.thirty_mins)
    
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def setup_task(self):
        interval = self.interval_schedule
        self.fecha_inicio = timezone.now()
        tiempo_total = (self.fecha_final - self.fecha_inicio).total_seconds() # Duracion del experimento en segundos
        self.cantidad_imagenes = int(tiempo_total/self.period_secs)+1
        self.task = PeriodicTask(
            name=self.nombre,
            task='experimentos.tasks.captura',
            interval=interval,
            args=json.dumps([self.id]),
            start_time=self.fecha_inicio,
            expires = self.fecha_final #+ timedelta(seconds=5)
            )
        self.task.enabled = True
        self.task.save()
        print("Task created!")
        self.save()
    
    @property
    def interval_schedule(self):
        if self.time_interval == TimeInterval.fifteen_mins:
            self.period_secs = 15*60
            return IntervalSchedule.objects.create(every=15, period='minutes')
        if self.time_interval == TimeInterval.thirty_mins:
            self.period_secs = 30*60
            return IntervalSchedule.objects.create(every=30, period='minutes')
        if self.time_interval == TimeInterval.one_hour:
            self.period_secs = 60*60
            return IntervalSchedule.objects.create(every=1, period='hours')
        if self.time_interval == TimeInterval.two_hours:
            self.period_secs = 2*60*60
            return IntervalSchedule.objects.create(every=2, period='hours')
        if self.time_interval == TimeInterval.three_hours:
            self.period_secs = 3*60*60
            return IntervalSchedule.objects.create(every=3, period='hours')
        if self.time_interval == TimeInterval.ten_seconds:
            self.period_secs = 10
            return IntervalSchedule.objects.create(every=10, period='seconds')
        
        raise NotImplementedError


    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

@receiver(post_save, sender=Experimento)
def create_or_update_periodic_task(sender, instance, created, **kwargs):
    if created:
        instance.dish.is_available = False
        instance.setup_task()
    # else:
    #     if instance.task is not None:
    #         instance.task.save()

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
