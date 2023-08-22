from typing import Any, Dict
import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from core.views import UUIDViewMixin
from ocorrencias.models import Ocorrencia
from adolescentes.models import Adolescente
from unidades.models import Unidade


def unidade_filterset(request):
    if "adolescente_uuid" in request.resolver_match.kwargs:
        adolescente = Adolescente.objects.get(uuid=request.resolver_match.kwargs.get("adolescente_uuid"))
        id_unidades = adolescente.entradas_em_unidades.all().values_list('unidade__id', flat=True)
        return Unidade.objects.filter(id__in=id_unidades)
    
    return Unidade.objects.none()


class OcorrenciaProntuarioFilterSet(django_filters.FilterSet): 
    PARTICIPACAO_CHOICES = (
        ('Autor', 'Autor'),
        ('Vítima', 'Vítima'),
    ) 
    participacao = django_filters.ChoiceFilter(choices=PARTICIPACAO_CHOICES, empty_label="Todas", label="Participação")
    
    unidade = django_filters.ModelChoiceFilter(
        label="Unidade",
        queryset=unidade_filterset,
        empty_label="Todas",
    )


class OcorrenciaProntuarioListView(
    LoginRequiredMixin, 
    ListView
):
    model = Ocorrencia
    template_name = "prontuario/ocorrencia/ocorrencia_list.html"
    paginate_by = 20
    
    def get_queryset(self, *args, **kwargs):
        from django.db.models import Value
        adolescente = Adolescente.objects.get(uuid=self.kwargs['adolescente_uuid'])
        como_vitima = adolescente.ocorrencias_como_vitima.annotate(participacao=Value('Vítima'))
        como_autor = adolescente.ocorrencias_como_autor.annotate(participacao=Value('Autor'))
        
        self.filterset = OcorrenciaProntuarioFilterSet(self.request.GET, request=self.request, queryset=como_vitima)
        self.filterset_2 = OcorrenciaProntuarioFilterSet(self.request.GET, request=self.request, queryset=como_autor)
        return self.filterset.qs.union(self.filterset_2.qs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class OcorrenciaProntuarioDetailView(
    LoginRequiredMixin, 
    UUIDViewMixin,
    DetailView
):
    model = Ocorrencia
    uuid_url_kwarg = "ocorrencia_uuid"
    template_name = "prontuario/ocorrencia/ocorrencia_detail.html"
        
    



