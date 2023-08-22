from django.views import View
from django.shortcuts import render
from estatistica.dash.geral.dashboard_total_situacao_escolar_por_unidade import Dashboard


class DashboardAvancadoSituacaoEscolarPorUnidade(View):
    def get(self, request, *args, **kwargs):
        Dashboard.situacao_escolar_por_unidade()
        return render(
            self.request,
            'estatistica/dashboard/dashboard_avancado_situacao_escolar_por_unidade.html',
        )
