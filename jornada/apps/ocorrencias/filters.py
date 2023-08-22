import django_filters
from django.db.models import Q
from .models import Ocorrencia


def multiple_search(queryset, name, value):
    queryset = queryset.filter(Q(adolescentes_autores__nome__icontains=value))
    return queryset


class OcorrenciaFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(label="Buscar", method=multiple_search)
    data = django_filters.DateTimeFilter(label="Data e Hora", field_name="data_hora")

    class Meta:
        model = Ocorrencia
        fields = ("busca",)
