from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from unidades.views import EntradaAdolescenteLotadosListView
from core.views import FilteredViewMixin
from unidades.filters import UamaAdolescenteListFilterSet


class AdolescenteListView(
    LoginRequiredMixin, 
    FilteredViewMixin,
    EntradaAdolescenteLotadosListView,
):
    template_name: str = 'uama/adolescente_list.html'
    filterset_class = UamaAdolescenteListFilterSet

    def get_queryset(self):
        qs = super().get_queryset().filter(
            modulo__uuid=self.kwargs.get('modulo_uuid'),
        )
        return qs.order_by('modulo', 'adolescente__nome')