import django_filters
from django.db.models import Q


from .models import  Modulo, Quarto, Unidade
from unidades.models import Unidade


def multiple_search(queryset, name, value):
    return queryset.filter(Q(adolescente__nome__unaccent__icontains=value))


def quarto_filterset(request):

    if "modulo_uuid" in request.resolver_match.kwargs:
        modulo = Modulo.objects.get(uuid=request.resolver_match.kwargs.get("modulo_uuid"))
        return modulo.quartos.all()

    if "unidade_uuid" in request.resolver_match.kwargs:
        qts = Quarto.objects.filter(modulo__unidade__uuid=request.resolver_match.kwargs.get("unidade_uuid"))
        return qts
    
    return Quarto.objects.none()




class UamaAdolescenteListFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(label="Buscar Adolescente", method=multiple_search)
    

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

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You need to override the label_from_instance method in the filter's form field
       
        
