import django_filters
from django.db.models import Q
from core.filters import DateRangeFilter

from .models import Vinculacao, Transferencia, Desvinculacao

def multiple_search(queryset, name, value):
    queryset = queryset.filter(Q(adolescente__nome__icontains=value))
    return queryset

class VinculacaoFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(
        label='Buscar', 
        method=multiple_search
    )

    status = django_filters.ChoiceFilter(
        label="Status:",
        choices=Vinculacao.Status.choices,
        empty_label="Todos"
    )
    periodo = DateRangeFilter(empty_label="----------", label="Data", field_name="data")

class TransferenciaFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(
        label='Buscar',
        method=multiple_search
    )
    
    status = django_filters.ChoiceFilter(
        label="Status",
        choices=Transferencia.Status.choices,
        empty_label="Todos"
    )
    periodo = DateRangeFilter(empty_label="----------", label="Data", field_name="data")
    
class DesvinculacaoFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(
        label='Buscar',
        method=multiple_search
    )

    status = django_filters.ChoiceFilter(
        label="Status", 
        choices=Desvinculacao.Status.choices,
        empty_label="Todos"
    )
    periodo = DateRangeFilter(empty_label="----------", label="Data", field_name="data")