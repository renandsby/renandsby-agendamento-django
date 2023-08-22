from django.views import View
from django.shortcuts import render
from estatistica.dash.adolescentes.adolescentes_por_unidade_internacao import (
    dashboard_adolescente_por_unidade_internacao,
)


class DashboardEspecificoInternacaoUnidades(View):
    def get(self, request, *args, **kwargs):
        dashboard_adolescente_por_unidade_internacao()
        return render(
            self.request, 'estatistica/dashboard/dashboard_especifico_internacao_unidades.html'
        )
