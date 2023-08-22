from django.contrib import admin
from .models import Atividade, HistoricoAtividade, AdolescenteAtividade, AnexoHistoricoAtividade


class AdolescenteAtividadeInline(admin.StackedInline):
    model = AdolescenteAtividade
    extra = 1

class AtividadeAdmin(admin.ModelAdmin):
    model = Atividade
    inlines = [AdolescenteAtividadeInline]
    list_display = ["__str__", "unidade",]
    list_filter = ("unidade",)

class AnexoHistoricoAtividadeInline(admin.StackedInline):
    model = AnexoHistoricoAtividade
    extra = 1

class HistoricoAtividadeAdmin(admin.ModelAdmin):
    @admin.display(description='Unidade')
    def get_unidade(self, obj):
        return obj.modulo.unidade
    
    @admin.display(description='Retorno')
    def get_retorno(self, obj):
        if obj.retorno_indeterminado:
            return "Indeterminado/Não retornou"
        return obj.data_retorno    
    
    @admin.display(description='Ida')
    def get_ida(self, obj):
        if not obj.data_ida and obj.agendado:
            return "Agendado para: " + str(obj.data_prevista_ida)
        return obj.data_ida
    
    model = HistoricoAtividade
    inlines = [AnexoHistoricoAtividadeInline]
    list_display = ["adolescente", "atividade", "get_unidade", "get_ida", "get_retorno", "realizada", "em_atividade"]
    list_filter = ( "data_ida", "modulo__unidade", "realizada", "em_atividade")
    


admin.site.register(Atividade, AtividadeAdmin)
admin.site.register(HistoricoAtividade, HistoricoAtividadeAdmin)
