import django_filters
from django.db.models import Q
from dominios.models import TipoAtividade
from adolescentes.models import Adolescente
from atividades.models import Atividade
from unidades.models import Unidade, Modulo
from core.filters import DateRangeFilter, CustomChoiceFilter

def multiple_search(queryset, name, value):
    return queryset.filter(Q(descricao__icontains=value))


class AtividadeFilterSet(django_filters.FilterSet):

    busca = django_filters.CharFilter(label='Buscar', method=multiple_search)

    tipo_atividade = django_filters.ModelChoiceFilter(
        label="Tipo de Atividade", queryset=TipoAtividade.objects.all(), empty_label="Todos"
    )

def OpcoesAdolescente(request):
    if request is None:
        return Adolescente.objects.none()
    if 'unidade_uuid' in request.resolver_match.kwargs:
        unidade = Unidade.objects.get(uuid=request.resolver_match.kwargs.get('unidade_uuid'))
        return Adolescente.objects.filter(id__in=unidade.ids_adolescentes_lotados)
    
    if 'modulo_uuid' in request.resolver_match.kwargs:    
        modulo = Modulo.objects.get(uuid=request.resolver_match.kwargs.get('modulo_uuid'))
        return Adolescente.objects.filter(id__in=modulo.ids_adolescentes_lotados)

    return Adolescente.objects.none()

def OpcoesAtividade(request):
    if request is None:
        return Atividade.objects.none()
    if 'unidade_uuid' in request.resolver_match.kwargs:
        return Atividade.objects.filter(unidade_uuid=request.resolver_match.kwargs['unidade_uuid'])
    if 'modulo_uuid' in request.resolver_match.kwargs:
        modulo = Modulo.objects.get(uuid=request.resolver_match.kwargs.get('modulo_uuid'))
        return Atividade.objects.filter(unidade=modulo.unidade)
    return Atividade.objects.none()



class AgendamentoFilterset(django_filters.FilterSet):
    adolescente = django_filters.ModelChoiceFilter(
        label="Adolescente", queryset=OpcoesAdolescente, empty_label="Todos"
    )
    atividade = django_filters.ModelChoiceFilter(
        label="Atividade", queryset=OpcoesAtividade, empty_label="Todos"
    )

    data_inicio = django_filters.DateFilter(label="Data Início", field_name='data_prevista_ida', lookup_expr=('date__gte')) 
    data_final = django_filters.DateFilter(label="Data Fim", field_name='data_prevista_ida', lookup_expr=('date__lte'))
    periodo = DateRangeFilter(empty_label="Todos", label="Período", field_name="data_prevista_ida")   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['atividade'].field.label_from_instance = lambda obj: obj.descricao


class SituacaoHistoricoFilter(CustomChoiceFilter):
    choices = [
        ('realizada', 'Atividade Realizada'),
        ('em_atividade', 'Em Atividade'),
    ]

    filters = {
        'realizada': lambda qs, name: qs.filter(realizada=True),
        'em_atividade': lambda qs, name: qs.filter(em_atividade=True),
    }



class HistoricoFilterset(django_filters.FilterSet):
    adolescente = django_filters.ModelChoiceFilter(
        label="Adolescente", queryset=OpcoesAdolescente, empty_label="Todos"
    )
    situacao = SituacaoHistoricoFilter(label="Situação", empty_label="Todas")
    periodo = DateRangeFilter(empty_label="Todas", label="Data", field_name="data_ida")
        
