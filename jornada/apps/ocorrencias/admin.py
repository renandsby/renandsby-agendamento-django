from django.contrib import admin
from .models import Ocorrencia, AnexoOcorrencia


class AnexoOcorrenciaInline(admin.TabularInline):
    model = AnexoOcorrencia
    extra = 1


class OcorrenciaAdmin(admin.ModelAdmin):
    model = Ocorrencia
    inlines = [AnexoOcorrenciaInline]
    list_display = ["__str__", "unidade", "modulo",]
    list_filter = ("data_hora", "unidade")

admin.site.register(Ocorrencia, OcorrenciaAdmin)
