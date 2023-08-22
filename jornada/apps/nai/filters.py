import django_filters
from dominios.models import TipoEntradaUnidade


class EfetivoNaiFilterSet(django_filters.FilterSet):
 
    tipo_entrada =  django_filters.ModelChoiceFilter(
        label = "Tipo de Entrada",
        queryset = TipoEntradaUnidade.objects.all(),
        empty_label = "Todos"
    )
