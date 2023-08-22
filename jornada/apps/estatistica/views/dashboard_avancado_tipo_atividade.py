from django.views import View
from django.shortcuts import render
from estatistica.dash.geral.dashboard_total_tipo_atividade import Dashboard


class DashboardAvancadoTipoAtividade(View):
    def get(self, request, *args, **kwargs):
        Dashboard.tipo_atividade()
        return render(self.request, 'estatistica/dashboard/dashboard_avancado_tipo_atividade.html')
