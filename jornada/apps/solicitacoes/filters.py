import django_filters
from django.db.models import Q
from .models import Solicitacao
from dominios.models import AcaoSolicitacaoMovimentacao

from core.filters import DateRangeFilter

def multiple_search(queryset, name, value):
    queryset = queryset.filter(
        Q(nome_adolescente__icontains=value) |
        Q(adolescente__nome__icontains=value) |
        Q(numero_processo__icontains=value) |
        Q(processo__numero__icontains=value))

    return queryset

class SolicitacaoFilterSet(django_filters.FilterSet):
    
    busca = django_filters.CharFilter(
        label='Buscar',
        method=multiple_search
    )

    acao_solicitada =  django_filters.ModelChoiceFilter(
        label="Ação Solicitada",
        queryset=AcaoSolicitacaoMovimentacao.objects.all(),
        empty_label="Todos"
    )

    status = django_filters.ChoiceFilter(
        label="Status",
        choices=Solicitacao.Status.choices,
        empty_label="Todos"
    )
    periodo = DateRangeFilter(empty_label="----------", label="Data", field_name="criado_em")