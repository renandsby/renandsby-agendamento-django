from unidades.models import Unidade, Modulo



def url_kwargs_object_injection(request):
    context = {}
    

    if 'unidade_uuid' in request.resolver_match.kwargs:
        context['unidade'] = Unidade.objects.get(uuid=request.resolver_match.kwargs.get('unidade_uuid'))
    if 'modulo_uuid' in request.resolver_match.kwargs:
        context['modulo'] = Modulo.objects.get(uuid=request.resolver_match.kwargs.get('modulo_uuid'))



    return context