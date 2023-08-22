from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import CustomUser
from servidores.models import Servidor

# Register your models here.
class ServidorInline(admin.StackedInline):
    model = Servidor
    fk_name = "user"
    extra = 0
    

class UserAdmin(BaseUserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }

            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True


        return form
    
    
    @admin.display(description='Unidade')
    def get_unidade(self, obj):
        return obj.servidor.unidade

    @admin.display(description='Nome')
    def get_nome(self, obj):
        return obj.servidor.nome

    @admin.display(description='Denominação Função')
    def get_denominacao_funcao(self, obj):
        return obj.servidor.denominacao_funcao
    
    @admin.display(description='Matrícula')
    def get_matricula(self, obj):
        return obj.servidor.matricula
    
    @admin.display(description='Lotação')
    def get_lotacao(self, obj):
        if (obj.servidor.codigo_lotacao is not None
            and obj.servidor.descricao_lotacao is not None ):
            return obj.servidor.codigo_lotacao + " - " + obj.servidor.descricao_lotacao
        return None
    
    @admin.display(description='Grupos')
    def get_grupos(self, user):
        return ', '.join([str(g.name) for g in user.groups.all()])
    
    
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "change_password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    
    list_display = ("username", "get_nome", "get_matricula", "get_grupos", "get_unidade", "get_lotacao", 'get_denominacao_funcao')
    list_filter = ("servidor__unidade__sigla", "groups", "is_staff")
    search_fields = ("username__icontains","servidor__nome__icontains", "email", "servidor__unidade__sigla__icontains", "servidor__matricula__icontains")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    inlines = [ServidorInline]
    
admin.site.register(CustomUser, UserAdmin)