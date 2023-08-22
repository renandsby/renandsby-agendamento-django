from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse

from processos.views import (
    ProcessoCreateView,
    ProcessoListView,
    ProcessoUpdateView,
    ProcessoDeleteView
)
from .prontuario_base import (
    AdolescenteFilterMixin,
    AdolescenteFormBindMixin
)





class ProcessoProntuarioListView(
    LoginRequiredMixin,
    AdolescenteFilterMixin,
    ProcessoListView
):
    template_name = "prontuario/processo/processo_list.html"


class ProcessoProntuarioCreateView(
    LoginRequiredMixin, 
    AdolescenteFormBindMixin,
    ProcessoCreateView
):
    template_name = "prontuario/processo/processo_form.html"

    def get_success_url(self):
        return reverse('prontuario:processo-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})


class ProcessoProntuarioUpdateView(
    LoginRequiredMixin,
    ProcessoUpdateView
):
    template_name = "prontuario/processo/processo_form.html"

    def get_success_url(self):
        return reverse('prontuario:processo-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})


class ProcessoProntuarioDeleteView(
    LoginRequiredMixin,
    ProcessoDeleteView
):
    
    def get_success_url(self):
        return reverse('prontuario:processo-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})

