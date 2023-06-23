from django.contrib import admin
from .models import Experimento, PetriDish
# Register your models here.


class experimentoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "fecha_inicio", "fecha_final", "status", "dish"]

admin.site.register(Experimento, experimentoAdmin)

class petridishAdmin(admin.ModelAdmin):
    list_display = ["number", "is_available"]

admin.site.register(PetriDish, petridishAdmin)