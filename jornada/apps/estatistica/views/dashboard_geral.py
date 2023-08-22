from django.views import View
from django.shortcuts import render
from estatistica.dash.geral.dashboard import Dashboard


class DashboardGeral(View):
    def get(self, request, *args, **kwargs):
        Dashboard.por_unidade()
        #        return render(self.request,'estatistica/dashboard/dashboard_teste.html')

        return render(self.request, 'estatistica/dashboard/dashboard_geral.html')
