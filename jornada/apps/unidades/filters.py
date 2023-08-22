import django_filters
from django.db.models import Q

from dominios.models import TipoEntradaUnidade, TipoVagaUnidade
from .models import EntradaAdolescente, Modulo, Quarto, Unidade
from processos.models import Processo
from adolescentes.models import Adolescente
from unidades.models import Unidade


def multiple_search(queryset, name, value):
    return queryset.filter(Q(adolescente__nome__unaccent__icontains=value))


def tipo_entrada_filterset(request):

    if "modulo_uuid" in request.resolver_match.kwargs:
        id_tipo_entrada = (
            Modulo.objects.get(uuid=request.resolver_match.kwargs.get("modulo_uuid"))
            .entradas_atuais.all()
            .values_list("tipo_entrada_id", flat=True)
        )
        id_tipo_entrada = list(set(id_tipo_entrada))
        return TipoEntradaUnidade.objects.filter(id__in=id_tipo_entrada)

    if "unidade_uuid" in request.resolver_match.kwargs:
        id_tipo_entrada = (
            Unidade.objects.get(uuid=request.resolver_match.kwargs.get("unidade_uuid"))
            .adolescentes_lotados_entradas.all()
            .values_list("tipo_entrada_id", flat=True)
        )
        id_tipo_entrada = list(set(id_tipo_entrada))
        return TipoEntradaUnidade.objects.filter(id__in=id_tipo_entrada)
    
    return TipoEntradaUnidade.objects.none()


def quarto_filterset(request):

    if "modulo_uuid" in request.resolver_match.kwargs:
        modulo = Modulo.objects.get(uuid=request.resolver_match.kwargs.get("modulo_uuid"))
        return modulo.quartos.all()

    if "unidade_uuid" in request.resolver_match.kwargs:
        qts = Quarto.objects.filter(modulo__unidade__uuid=request.resolver_match.kwargs.get("unidade_uuid"))
        return qts
    
    return Quarto.objects.none()

def tipo_vaga_queryset(request):

    if "modulo_uuid" in request.resolver_match.kwargs:
        modulo = Modulo.objects.get(uuid=request.resolver_match.kwargs.get("modulo_uuid"))
        
        return TipoVagaUnidade.objects.filter(id__in=modulo.entradas_atuais.values_list('tipo_vaga__id', flat=True))

    if "unidade_uuid" in request.resolver_match.kwargs:
        unidade = Unidade.objects.get(uuid=request.resolver_match.kwargs.get("unidade_uuid"))
        return TipoVagaUnidade.objects.filter(id__in=unidade.adolescentes_lotados_entradas.values_list('tipo_vaga__id', flat=True))
    
    return TipoVagaUnidade.objects.none()



class UamaAdolescenteListFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(label="Buscar Adolescente", method=multiple_search)
    
    tipo_vaga =  django_filters.ModelChoiceFilter(
        label = "Tipo vaga",
        queryset = tipo_vaga_queryset,
        empty_label = "Todos"
    )

def quarto_filterset(request):

    if "modulo_uuid" in request.resolver_match.kwargs:
        modulo = Modulo.objects.get(uuid=request.resolver_match.kwargs.get("modulo_uuid"))
        if modulo.quartos.count() > 1:    
            return modulo.quartos.all()

    return Quarto.objects.none()

def modulo_filterset(request):

    if "unidade_uuid" in request.resolver_match.kwargs:
        unidade = Unidade.objects.get(uuid=request.resolver_match.kwargs.get("unidade_uuid"))
        if unidade.modulos.count() > 1:
            return unidade.modulos.all()

    return Modulo.objects.none()


class EfetivoGeralFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(
        label='Buscar Adolescente',
        method=multiple_search
    )

    modulo = django_filters.ModelChoiceFilter(
        label="Módulo",
        queryset=modulo_filterset,
        empty_label="Todos",     
    )


class ListaGeralFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(
        label='Buscar Adolescente',
        method=multiple_search
    )

    tipo_vaga =  django_filters.ModelChoiceFilter(
        label = "Tipo vaga",
        queryset = tipo_vaga_queryset,
        empty_label = "Todos"
    )
    
    tipo_entrada = django_filters.ModelChoiceFilter(
        label="Tipo de Entrada",
        queryset=tipo_entrada_filterset,
        empty_label="Todos",
    )
    modulo = django_filters.ModelChoiceFilter(
        label="Módulo",
        queryset=modulo_filterset,
        empty_label="Todos",     
    )
    




class ModuloAdolescenteListFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(
        label='Buscar Adolescente',
        method=multiple_search
    )
    quarto = django_filters.ModelChoiceFilter(
        label="Quarto",
        queryset=quarto_filterset,
        empty_label="Todos",     
    )





def processo_queryset(request):

    if "adolescente_uuid" in request.resolver_match.kwargs:
        adolescente = Adolescente.objects.get(uuid=request.resolver_match.kwargs.get("adolescente_uuid"))
        return adolescente.processos.all()
    
    return Processo.objects.none()


def unidade_queryset(request):

    if "adolescente_uuid" in request.resolver_match.kwargs:
        adolescente = Adolescente.objects.get(uuid=request.resolver_match.kwargs.get("adolescente_uuid"))
        id_unidades = adolescente.entradas_em_unidades.all().values_list('unidade__id', flat=True)
        return Unidade.objects.filter(id__in=id_unidades)
    
    return Unidade.objects.none()


class HistoricoProntuarioFilterSet(django_filters.FilterSet):
    unidade = django_filters.ModelChoiceFilter(
        label="Unidade",
        queryset=unidade_queryset,
        empty_label="Todas",
    )
    processo = django_filters.ModelChoiceFilter(
        label="Processo",
        queryset=processo_queryset,
        empty_label="Todos",
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You need to override the label_from_instance method in the filter's form field
        self.filters['processo'].field.label_from_instance = lambda obj: obj.str_sem_nome()
        
