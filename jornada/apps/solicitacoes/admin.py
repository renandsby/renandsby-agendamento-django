from django.contrib import admin
from .models import Solicitacao, AnexoSolicitacao

class AnexoInline(admin.TabularInline):
    model = AnexoSolicitacao
    extra = 1


class SolicitacaoAdmin(admin.ModelAdmin):
    readonly_fields = ('criado_por', 'criado_em')
    model = Solicitacao
    inlines = [AnexoInline]

admin.site.register(Solicitacao, SolicitacaoAdmin)
