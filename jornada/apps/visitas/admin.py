from django.contrib import admin
from .models import Visita

class VisitaAdmin(admin.ModelAdmin):
    model = Visita


admin.site.register(Visita, VisitaAdmin)