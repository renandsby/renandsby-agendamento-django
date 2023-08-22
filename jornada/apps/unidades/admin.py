from django.contrib import admin
from .models import Unidade, VagaUnidade, Modulo, Quarto

class VagasInline(admin.StackedInline):
    model = VagaUnidade
    extra = 1

class ModuloInline(admin.StackedInline):
    model = Modulo
    extra = 0
    

class UnidadeAdmin(admin.ModelAdmin):
    model: Unidade
    inlines = [VagasInline, ModuloInline]




class QuartoInline(admin.StackedInline):
    model = Quarto
    extra = 0


class ModuloAdmin(admin.ModelAdmin):
    model = Modulo
    inlines = [QuartoInline]

class QuartoAdmin(admin.ModelAdmin):
    model = Quarto


admin.site.register(Unidade, UnidadeAdmin)
admin.site.register(Modulo, ModuloAdmin)
admin.site.register(Quarto)
