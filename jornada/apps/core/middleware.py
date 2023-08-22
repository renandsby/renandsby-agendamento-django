from django.db.models import signals
from functools import partial
from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve
from unidades.models import Unidade, Modulo

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
            



def servidor_da_unidade(user, unidade):
    if (hasattr(user, 'servidor') and
            user.servidor is not None and 
            user.servidor.unidade is not None and
            user.servidor.unidade == unidade
        ):
        return True
    return False

class PermissaoDeUnidadeMiddleware:
    
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):    
        resolver_match = resolve(request.path)
        
        if 'unidade_uuid' in resolver_match.kwargs:
            if request.user.has_perm('unidades.acessar_todas'):
                return self.get_response(request)
    
            unidade = Unidade.objects.get(uuid=resolver_match.kwargs.get('unidade_uuid'))
            
            if request.user.has_perm('unidades.acessar_todas_semiliberdades'):
                if unidade.tipo_unidade.descricao == "Semiliberdade":
                    return self.get_response(request)
            
            if request.user.has_perm('unidades.acessar_todas_geamas'):
                if unidade.tipo_unidade.descricao == "Meio Aberto":
                    return self.get_response(request)
            
            if request.user.has_perm('unidades.acessar_todas_internacoes'):
                if unidade.tipo_unidade.descricao in ("Internação", "Atendimento Inicial"):
                    return self.get_response(request)
                
            if not servidor_da_unidade(request.user, unidade):
                return redirect('/')    
            
        if 'modulo_uuid' in resolver_match.kwargs:
            if request.user.has_perm('unidades.acessar_todas'):
                return self.get_response(request)
            
            modulo = Modulo.objects.get(uuid=resolver_match.kwargs.get('modulo_uuid'))
            
            if request.user.has_perm('unidades.acessar_todas_semiliberdades'):
                if modulo.unidade.tipo_unidade.descricao == "Semiliberdade":
                    return self.get_response(request)
            
            if request.user.has_perm('unidades.acessar_todas_geamas'):
                if modulo.unidade.tipo_unidade.descricao == "Meio Aberto":
                    return self.get_response(request)
            
            if request.user.has_perm('unidades.acessar_todas_internacoes'):
                if modulo.unidade.tipo_unidade.descricao in ("Internação", "Atendimento Inicial"):
                    return self.get_response(request)
            
            if not servidor_da_unidade(request.user, modulo.unidade):
                return redirect('/')
        
        return self.get_response(request)
    
class PermissaoDeAdolescenteMiddleware:
    
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):    
        resolver_match = resolve(request.path)
        
        if 'adolescente_uuid' not in resolver_match.kwargs:
            return self.get_response(request)
    
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if request.user.has_perm('adolescentes.ver_todos'):
                return self.get_response(request)
        
            if request.user.has_perm('adolescentes.ver_da_unidade'):
                if hasattr(request.user, 'servidor') and request.user.servidor is not None and request.user.servidor.unidade is not None:
                    unidade = request.user.servidor.unidade
                    if unidade.entradas_de_adolescentes.filter(
                        status__in=[1,2,3], 
                        adolescente__uuid=resolver_match.kwargs.get('adolescente_uuid')
                    ).exists():
                        return self.get_response(request)
            
            return redirect('prontuario:adolescente-list')
                        
        
        if request.user.has_perm('adolescentes.editar_todos'):
            return self.get_response(request)
        
        if request.user.has_perm('adolescentes.editar_da_unidade'):
            if hasattr(request.user, 'servidor') and request.user.servidor is not None and request.user.servidor.unidade is not None:
                unidade = request.user.servidor.unidade
                if unidade.entradas_de_adolescentes.filter(
                    status__in=[1,2,3], 
                    adolescente__uuid=resolver_match.kwargs.get('adolescente_uuid')
                ).exists():
                    return self.get_response(request)
        
        return redirect('prontuario:adolescente-list')