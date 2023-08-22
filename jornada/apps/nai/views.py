from django.urls.base import reverse
from django.views.generic import ListView
from django.db.models import Count
from unidades.models import EntradaAdolescente, Modulo
from dominios.models import TipoVagaUnidade

from core.views import FilteredViewMixin
from django.contrib import messages

from unidades.views import (
    EditaQuartoView,
    SaidaView,
    IncluirAdolescenteEntradaView
)

from unidades.forms import EntradaCheckoutNAIForm

from .filters import EfetivoNaiFilterSet

class EfetivoNaiView(
    FilteredViewMixin,
    ListView
):
    model = EntradaAdolescente
    filterset_class = EfetivoNaiFilterSet
    template_name = 'nai/efetivo_geral.html'
    paginate_by = 30
    context_object_name = 'entradas'
    
    def get_queryset(self):
        return super().get_queryset().filter(
            modulo__uuid = self.kwargs.get('modulo_uuid'),
            lotado=True
        ).order_by('modulo', 'quarto', 'adolescente__nome')
            
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        modulo = Modulo.objects.get(uuid=self.kwargs.get('modulo_uuid'))
        queryset_sem_filtro = EntradaAdolescente.objects.filter(
            modulo=modulo,
            tipo_entrada__isnull=False,
            lotado=True
        )
        estatisticas = queryset_sem_filtro.values(
            'tipo_entrada__descricao', 'tipo_entrada__id'
        ).annotate(total=Count('tipo_entrada'))
        context['estatisticas'] = estatisticas
        return context


class NaiSaidaView(SaidaView):
    template_name = 'nai/saida-nai.html'
    form_class = EntradaCheckoutNAIForm
    
    def get_success_url(self):
        messages.success(self.request, f'{self.object.adolescente} colocado em Saídas Previstas')
        entrada = EntradaAdolescente.objects.get(uuid=self.kwargs.get("entrada_uuid"))
        return reverse('nai:efetivo-nai',kwargs={"modulo_uuid": entrada.modulo.uuid })
    

class NaiEditaQuartoView(EditaQuartoView):

    def get_success_url(self):
        return reverse('nai:efetivo-nai',kwargs={"modulo_uuid": self.kwargs.get("modulo_uuid")})
                       

class NaiIncluirAdolescenteEntradaView(IncluirAdolescenteEntradaView):
    template_name = "nai/nai_entrada_de_oficio.html"

    def get_success_url(self):
        modulo_nai = Modulo.objects.get(uuid=self.kwargs.get("modulo_uuid"))
        return reverse('nai:efetivo-nai',kwargs={"modulo_uuid": modulo_nai.uuid })
        



