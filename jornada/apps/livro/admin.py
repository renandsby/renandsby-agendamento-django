from django.contrib import admin

from .models import Livro, Acompanhamento, EfetivoLivro, AdolescenteEfetivoLivro

class AdolescenteEfetivoLivroInline(admin.StackedInline):
    model = AdolescenteEfetivoLivro
    extra = 0
    
class EfetivoLivroAdmin(admin.ModelAdmin):
    list_filter = ("livro__data_abertura", "livro__unidade", )
    list_display = ('__str__',) 
    inlines = [AdolescenteEfetivoLivroInline]


class AcompanhamentoInline(admin.StackedInline):
    model = Acompanhamento
    extra = 1

class LivroAdmin(admin.ModelAdmin):
    inlines = [AcompanhamentoInline]
    list_filter = ("data_abertura", "unidade",)
    list_display = ('__str__', "unidade", "modulo") 


admin.site.register(Livro, LivroAdmin)
admin.site.register(EfetivoLivro, EfetivoLivroAdmin)