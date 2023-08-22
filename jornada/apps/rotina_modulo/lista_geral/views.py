from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from core.views import FilteredViewMixin
from unidades.models import EntradaAdolescente,Unidade
from django.db.models import Count
from unidades.filters import ListaGeralFilterSet
    
        
class ListaGeralListView(
    LoginRequiredMixin, 
    FilteredViewMixin,
    ListView
):
    template_name = "rotina_modulo/lista_geral/lista_geral_list.html"
    model = EntradaAdolescente
    filterset_class = ListaGeralFilterSet
    paginate_by = 100
    
    def get_queryset(self):
        qs =  super().get_queryset().filter(
            unidade__uuid=self.kwargs['unidade_uuid'],
            modulo__isnull=False,
            lotado=True
        ).order_by('modulo', 'quarto')
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        queryset_sem_filtro = EntradaAdolescente.objects.filter(
            unidade__uuid=self.kwargs['unidade_uuid'],
            lotado=True,
            tipo_vaga__isnull=False
        )

        estatisticas =  queryset_sem_filtro.values(
            'tipo_vaga__descricao', 'tipo_vaga__id'
        ).annotate(total=Count('tipo_vaga'))
        
        
        context['estatisticas'] = estatisticas
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '')
        print(f"{ordering=}")
        return ordering