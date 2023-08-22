from django.shortcuts import render
from django.views import View
from estatistica.dash.adolescentes.adolescente_por_genero import \
    dashboard_adolescente_por_genero


class AdolescentePorGenero(View):
    def get(self, request, *args, **kwargs):
        dashboard_adolescente_por_genero()
        return render(
            self.request,
            "estatistica/dashboard/adolescente_por_genero.html",
        )
