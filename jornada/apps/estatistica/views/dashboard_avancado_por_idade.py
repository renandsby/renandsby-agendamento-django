from django.views import View
from django.shortcuts import render
from estatistica.dash.adolescentes.adolescentes_por_idade import dashboard_adolescente_por_idade


class DashboardAvancadoPorIdade(View):
    def get(self, request, *args, **kwargs):
        dashboard_adolescente_por_idade()
        return render(self.request, 'estatistica/dashboard/dashboard_avancado_por_idade.html')
