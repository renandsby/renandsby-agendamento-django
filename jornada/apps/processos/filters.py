import django_filters
from django.db.models import Q

def multiple_search(queryset, name, value):
    queryset = queryset.filter(
        Q(adolescente__nome__icontains=value) |
        Q(numero__icontains=value) |
        Q(vara__descricao__icontains=value) 
    )
    return queryset

class ProcessoFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(
        label='Buscar', 
        method=multiple_search
    )
    
