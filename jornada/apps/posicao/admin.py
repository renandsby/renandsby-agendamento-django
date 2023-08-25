from django.contrib import admin

from .models import RedeEmpresas, Endereco, Vagas


# class EnderecoInline(admin.StackedInline):
#     model = Endereco
#     extra = 1

# class VagasInline(admin.StackedInline):
#     model = Vagas
#     extra = 1
    

# class RedeEmpresasAdmin(admin.ModelAdmin):
#     model = RedeEmpresas
#     inlines = [VagasInline, EnderecoInline]
#     readonly_fields = ('criado_por', 'modificado_por', 'criado_em', 'modificado_em')
#     list_display = ["descricao"]
#     # search_fields = ("descricao__icontains")


# admin.site.register(RedeEmpresas,RedeEmpresasAdmin)
# Register your models here.
admin.site.register(RedeEmpresas)
admin.site.register(Endereco)
# admin.site.register(Vagas)