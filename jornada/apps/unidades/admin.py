from django.contrib import admin
from .models import Unidade, VagaUnidade, EntradaAdolescente, Modulo, Quarto, MedidaAdaptacao, MedidaDisciplinar, AnexoEntrada


class VagasInline(admin.StackedInline):
    model = VagaUnidade
    extra = 1

class ModuloInline(admin.StackedInline):
    model = Modulo
    extra = 0
    

class UnidadeAdmin(admin.ModelAdmin):
    model: Unidade
    inlines = [VagasInline, ModuloInline]



class AnexoEntradaInline(admin.StackedInline):
    model = AnexoEntrada
    extra = 0


class MedidaAdaptacaoInline(admin.StackedInline):
    model = MedidaAdaptacao
    readonly_fields = ('data_fim',)
    extra = 0

class MedidaDisciplinarInline(admin.StackedInline):
    model = MedidaDisciplinar
    readonly_fields = ('data_fim',)
    extra = 0

class EntradaAdolescenteAdmin(admin.ModelAdmin):
    @admin.display(description='Quarto')
    def get_quarto(self, obj):
        name = ""
        if obj.quarto is not None:
            if obj.unidade.modulos.count() > 1:
                name += "M" + obj.modulo.descricao +" - "
            
            name += str(obj.quarto.numero)
            if obj.quarto.nome is not None:
                name += obj.quarto.nome
            
        return name
    
    readonly_fields = ('lotado',)
    inlines = [MedidaAdaptacaoInline, MedidaDisciplinarInline, AnexoEntradaInline]
    list_filter = ("status", "unidade", 'tipo_vaga')
    list_display = ('__str__', 'data_prevista_entrada', 'data_entrada', 'tipo_vaga', 'data_prevista_saida', 'data_saida', 'get_quarto')

class QuartoInline(admin.StackedInline):
    model = Quarto
    extra = 0


class ModuloAdmin(admin.ModelAdmin):
    model = Modulo
    inlines = [QuartoInline]

class QuartoAdmin(admin.ModelAdmin):
    model = Quarto


admin.site.register(EntradaAdolescente, EntradaAdolescenteAdmin)
admin.site.register(Unidade, UnidadeAdmin)
admin.site.register(Modulo, ModuloAdmin)
admin.site.register(Quarto)
