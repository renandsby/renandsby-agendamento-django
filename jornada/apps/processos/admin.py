from django.contrib import admin
from .models import Processo, Decisao, AnexoProcesso



class DecisaoInline(admin.StackedInline):
    model = Decisao
    extra = 1


class AnexoProcessoInline(admin.TabularInline):
    model = AnexoProcesso
    extra = 2


class ProcessoAdmin(admin.ModelAdmin):
    @admin.display(description='Id Jornada')
    def get_id_jornada(self, obj):
        return obj.adolescente.id_jornada
    
    @admin.display(description='SIPIA')
    def get_sipia(self, obj):
        return obj.adolescente.sipia
    
    model = Processo
    inlines = [DecisaoInline, AnexoProcessoInline]
    list_display = ["numero", "adolescente", "get_id_jornada", "get_sipia", "numero_paai"]
    search_fields = (
        "numero__icontains", 
        "adolescente__nome__icontains", 
        "numero_paai__icontains", 
        "adolescente__id_jornada__icontains",
        "adolescente__sipia__icontains"
    )


admin.site.register(Processo, ProcessoAdmin)