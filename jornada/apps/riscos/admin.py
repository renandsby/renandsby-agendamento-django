from django.contrib import admin
from .models import Risco, AnexoRisco

class AnexoInline(admin.TabularInline):
    model = AnexoRisco
    extra = 0

class RiscoAdmin(admin.ModelAdmin):
    model = Risco
    inlines = [AnexoInline]


admin.site.register(Risco, RiscoAdmin)
