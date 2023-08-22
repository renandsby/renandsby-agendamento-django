from django.views import View
from django.shortcuts import render
from estatistica.dash.geral.dashboard_total_tipo_entrada import Dashboard


class DashboardAvancadoTipoEntrada(View):
    def get(self, request, *args, **kwargs):
        Dashboard.tipo_entrada()
        return render(self.request, 'estatistica/dashboard/dashboard_avancado_tipo_entrada.html')
