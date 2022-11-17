from django.contrib import admin
from .models import Experimento
# Register your models here.


class experimentoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "fecha_inicio", "fecha_final", "status"]

admin.site.register(Experimento, experimentoAdmin)