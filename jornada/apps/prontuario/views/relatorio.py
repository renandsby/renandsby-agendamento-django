from django.views.generic import DeleteView

from adolescentes.views import (
    RelatorioCreateView, 
    RelatorioListView, 
    RelatorioUpdateView
)
from adolescentes.models import Relatorio
from core.views import UUIDViewMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse

from .prontuario_base import AdolescenteFilterMixin, AdolescenteFormBindMixin


class RelatorioProntuarioListView(
    LoginRequiredMixin, 
    AdolescenteFilterMixin, 
    RelatorioListView
):
    template_name = "prontuario/relatorios/relatorios_list.html"
    
    
class RelatorioProntuarioCreateView(
    LoginRequiredMixin, 
    AdolescenteFormBindMixin, 
    RelatorioCreateView
):
    template_name = "prontuario/relatorios/relatorios_form.html"

    def get_success_url(self):
        return reverse(
            "prontuario:relatorio-list", 
            kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")},
        )


class RelatorioProntuarioUpdateView(
    LoginRequiredMixin, 
    RelatorioUpdateView
):
    template_name = "prontuario/relatorios/relatorios_form.html"
    
    def get_success_url(self):
        return reverse(
            "prontuario:relatorio-list", 
            kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")},
        )


class RelatorioProntuarioDeleteView(
    UUIDViewMixin,
    DeleteView
):
    model = Relatorio
    http_method_names = ['delete', 'post']
    uuid_url_kwarg = 'relatorio_uuid'

    def form_valid(self, form):
        from django.contrib import messages
        from django.shortcuts import redirect
        
        try:
            self.object.delete()
            messages.success(self.request, f'{self.object.__class__.__name__} deletado com sucesso.')
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(self.request, f'{self.object.__class__.__name__} não pôde ser deletado. {get_error_message(e)}')
            return redirect(self.request.META.get('HTTP_REFERER'))
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse(
            "prontuario:relatorio-list", 
            kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")},
        )
