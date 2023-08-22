from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from unidades.models import EntradaAdolescente
from core.views import FilteredViewMixin
from .prontuario_base import AdolescenteFilterMixin
from unidades.filters import HistoricoProntuarioFilterSet

class HistoricoListView(
    LoginRequiredMixin, 
    FilteredViewMixin,
    AdolescenteFilterMixin,
    ListView
):

    model = EntradaAdolescente
    filterset_class = HistoricoProntuarioFilterSet
    paginate_by = 20
    template_name = "prontuario/historico/historico_list.html"



