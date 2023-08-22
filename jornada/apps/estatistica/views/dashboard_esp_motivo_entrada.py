from django.views import View
from django.shortcuts import render
from estatistica.dash.adolescentes.adolescentes_motivo_entrada import dashboard_adolescente_motivo_entrada


class DashboardEspMotivoEntrada(View):
    def get(self, request, *args, **kwargs):
        dashboard_adolescente_motivo_entrada()
        return render(
            self.request, 'estatistica/dashboard/dashboard_esp_tipo_entrada.html'
        )
