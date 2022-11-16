from django.contrib import admin
from .models import Experimento
# Register your models here.


class experimentoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "fecha_inicio"]

admin.site.register(Experimento, experimentoAdmin)