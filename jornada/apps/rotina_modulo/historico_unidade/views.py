from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from core.views import FilteredViewMixin
from unidades.models import EntradaAdolescente
from dominios.models import TipoEntradaUnidade
import django_filters
from django.db.models import Q
from core.filters import DateRangeFilter


def multiple_search(queryset, name, value):
    queryset = queryset.filter(Q(adolescente__nome__icontains=value))
    return queryset

class HistoricoFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(
        label='Buscar',
        method=multiple_search
    )
    
    tipo_entrada =  django_filters.ModelChoiceFilter(
        label = "Tipo de Entrada",
        queryset = TipoEntradaUnidade.objects.all(),
        empty_label = "Todos"
    )
     
    periodo = DateRangeFilter(empty_label="----------", label="Data Entrada", field_name="data_entrada")
    
        
        
class HistoricoUnidadeListView(
    LoginRequiredMixin, 
    FilteredViewMixin,
    ListView
):
    template_name = "rotina_modulo/historico_unidade/historico_unidade_list.html"
    model = EntradaAdolescente
    context_object = 'entradas_list'
    paginate_by = 40
    filterset_class = HistoricoFilterSet

    def get_queryset(self):
        qs =  super().get_queryset().filter(
            unidade__uuid=self.kwargs['unidade_uuid']
        )
        
        from django.db.models import F 
        if not self.get_ordering():
            qs = qs.order_by(
                    F('data_prevista_entrada').desc(nulls_last=True),
                    F('data_entrada').desc(nulls_last=True),
            )
        
        return qs
    
    
    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '')
        print(f"{ordering=}")
        return ordering