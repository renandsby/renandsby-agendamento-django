from django.views import View
from django.shortcuts import render
from estatistica.dash.adolescentes.atividades import dashboard_atividades


class DashboardEspAtividades(View):
    def get(self, request, *args, **kwargs):
        dashboard_atividades()
        return render(self.request, 'estatistica/dashboard/dashboard_esp_atividades.html')
