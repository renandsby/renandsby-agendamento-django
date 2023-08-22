from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from urllib.parse import urlparse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url


ADOLESCENTE_PK_URL_KWARG = "adolescente_id"
UNIDADE_PK_URL_KWARG = "unidade_uuid"

class SomenteAdministradorECentralMixin(AccessMixin):
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        # Se o usuário for administrador ou central ou superusuário, pode acessar 
        if  (user.groups.filter(name="Administrador").exists() or 
             user.groups.filter(name="Central").exists() or 
             user.is_superuser):

            #TODO tela de acesso negado
            return super().dispatch(request, *args, **kwargs)
        
        else:  
            return self.handle_no_permission()

class FiltraAdolescentes:
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        if user.has_perm('adolescentes.ver_todos'):
            return queryset
        
        if user.has_perm('adolescentes.ver_da_unidade'):
            if user.servidor is not None and user.servidor.unidade is not None:
                ids = user.servidor.unidade.entradas_de_adolescentes.filter(status__in=[1,2,3]).values_list('adolescente__id', flat=True)
                return queryset.filter(id__in=ids)
               
        return queryset.none()

class CustomPermissionMixin(PermissionRequiredMixin):
    redirect_to_login = False
    raise_exception = False
    no_permission_redirect_url = None
    check_permission_only_in_post = False
    
    def get_no_permission_redirect_url(self):
        if self.no_permission_redirect_url is None:
            referer = self.request.META.get('HTTP_REFERER')
            if referer is not None:
                return referer
            return '/'
        return self.no_permission_redirect_url
    
    def has_permission(self):
        if self.check_permission_only_in_post:
            if self.request.method != "POST":
                return True
            
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)
    
    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())

        messages.error(self.request, f'Você não possui permissão para realizar essa ação.')
        
        if not self.redirect_to_login:
            return redirect(self.get_no_permission_redirect_url())
        
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )