from unidades.models import Unidade, Modulo, EntradaAdolescente
from adolescentes.models import Adolescente


def url_kwargs_object_injection(request):
    context = {}
    
    if 'adolescente_uuid' in request.resolver_match.kwargs:
        context['adolescente'] = Adolescente.objects.get(uuid=request.resolver_match.kwargs.get('adolescente_uuid'))

    if 'unidade_uuid' in request.resolver_match.kwargs:
        context['unidade'] = Unidade.objects.get(uuid=request.resolver_match.kwargs.get('unidade_uuid'))
    if 'modulo_uuid' in request.resolver_match.kwargs:
        context['modulo'] = Modulo.objects.get(uuid=request.resolver_match.kwargs.get('modulo_uuid'))
    if 'entrada_uuid' in request.resolver_match.kwargs:
        context['entrada'] = EntradaAdolescente.objects.get(uuid=request.resolver_match.kwargs.get('entrada_uuid'))
    if 'rede_uuid' in request.resolver_match.kwargs:
        context['rede_uuid'] = UnidadeDeApoio.objects.get(uuid=request.resolver_match.kwargs.get('rede_uuid'))

    return context