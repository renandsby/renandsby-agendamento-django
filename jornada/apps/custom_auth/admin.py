from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import CustomUser


    

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
    
    list_display = ("username",  "get_grupos")
    list_filter = ( "groups", "is_staff")
    search_fields = ("username__icontains", "email",)
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
  
    
admin.site.register(CustomUser, UserAdmin)