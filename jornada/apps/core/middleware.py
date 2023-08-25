from django.db.models import signals
from functools import partial
from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve


class AuthoringMiddleware:
    '''
    Middleware que intercepta a criação ou atualização de objetos
    e automaticamente preenche os campos criado_por e modificado_por
    '''

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        if not request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if hasattr(request, 'user') and request.user.is_authenticated:
                user = request.user
            else:
                user = None

            save_author = partial(self.save_author, user)
            signals.pre_save.connect(
                save_author,
                dispatch_uid=(
                    self.__class__,
                    request,
                ),
                weak=False,
            )

        response = self.get_response(request)

        signals.pre_save.disconnect(
            dispatch_uid=(
                self.__class__,
                request,
            )
        )
        return response

    def save_author(self, user, sender, instance, **kwargs):
        if hasattr(instance, 'criado_por') and not instance.id:
            instance.criado_por = user

        if hasattr(instance, 'modificado_por'):
            instance.modificado_por = user
            






class PermissaoDeAdolescenteMiddleware:
    
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):    
        resolver_match = resolve(request.path)
        
        if 'adolescente_uuid' not in resolver_match.kwargs:
            return self.get_response(request)
    
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            
        
           
            
            return redirect('prontuario:adolescente-list')
                        
        
        
        return redirect('prontuario:adolescente-list')