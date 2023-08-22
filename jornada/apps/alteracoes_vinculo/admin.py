from django.contrib import admin

from .models import Transferencia, Desvinculacao, Vinculacao, AnexoVinculacao, AnexoTransferencia, AnexoDesvinculacao

class AnexoVinculacaoInline(admin.TabularInline):
    model = AnexoVinculacao

class AnexoDesvinculacaoInline(admin.TabularInline):
    model = AnexoDesvinculacao

class AnexoTransferenciaInline(admin.TabularInline):
    model = AnexoTransferencia

class TransferenciaAdmin(admin.ModelAdmin):
    inlines = [AnexoTransferenciaInline]

class DesvinculacaoAdmin(admin.ModelAdmin):
    inlines = [AnexoDesvinculacaoInline]

class VinculacaoAdmin(admin.ModelAdmin):
    inlines = [AnexoVinculacaoInline]

admin.site.register(Vinculacao, VinculacaoAdmin)
admin.site.register(Transferencia, TransferenciaAdmin)
admin.site.register(Desvinculacao, DesvinculacaoAdmin)
