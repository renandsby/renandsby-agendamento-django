from django.views import View
from django.shortcuts import render
from estatistica.dash.educacao.situacao_escolar import dashboard_situacao_escolar


class DashboardEspSituacaoEscolar(View):
    def get(self, request, *args, **kwargs):
        dashboard_situacao_escolar()
        return render(
            self.request,
            'estatistica/dashboard/dashboard_esp_situacao_escolar.html',
        )
