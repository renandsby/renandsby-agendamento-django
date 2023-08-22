from django.views import View
from django.shortcuts import render
from estatistica.dash.geral.dashboard_total_situacao_escolar_por_ra import Dashboard


class DashboardAvancadoSituacaoEscolarPorRa(View):
    def get(self, request, *args, **kwargs):
        Dashboard.situacao_escolar_por_ra()
        return render(
            self.request,
            'estatistica/dashboard/dashboard_avancado_situacao_escolar_por_ra.html',
        )
