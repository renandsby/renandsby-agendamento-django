from django.contrib import admin
from .models import AtendimentoPsicossocial, AnexoAtendimento


class AnexoAtendimentoInline(admin.TabularInline):
    model = AnexoAtendimento
    extra = 1


class AtendimentoAdmin(admin.ModelAdmin):
    model = AtendimentoPsicossocial
    inlines = [AnexoAtendimentoInline]

admin.site.register(AtendimentoPsicossocial, AtendimentoAdmin)
