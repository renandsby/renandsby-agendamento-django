from django.contrib import admin
from .models import Adolescente, Endereco, Telefone, Foto, Familiar, DocumentoAnexo
from processos.models import Processo


class DocumentoAnexoInline(admin.TabularInline):
    model = DocumentoAnexo
    extra = 1

class FamiliarInline(admin.TabularInline):
    model = Familiar
    extra = 1

class EnderecoInline(admin.StackedInline):
    model = Endereco
    extra = 1

class TelefoneInline(admin.TabularInline):
    model = Telefone
    extra = 1

class FotoInline(admin.TabularInline):
    model = Foto
    extra = 1

class ProcessoInline(admin.TabularInline):
    model = Processo
    extra = 1

class AdolescenteAdmin(admin.ModelAdmin):
    model = Adolescente
    inlines = [DocumentoAnexoInline, FamiliarInline, TelefoneInline, FotoInline, EnderecoInline, ProcessoInline]
    readonly_fields = ('criado_por', 'modificado_por', 'criado_em', 'modificado_em')
    list_display = ["nome", "data_nascimento", "nome_mae", "sipia", "id_jornada"]
    search_fields = ("sipia__icontains", "id_jornada__icontains", "nome__icontains", "nome_mae__icontains")


admin.site.register(Adolescente, AdolescenteAdmin)

