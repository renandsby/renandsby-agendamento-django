
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from riscos.views import (
    RiscoCreateView,
    RiscoListView,
    RiscoUpdateView
)
from .prontuario_base import (
    AdolescenteFilterMixin,
    AdolescenteFormBindMixin
)

class RiscoProntuarioListView(
    LoginRequiredMixin,
    AdolescenteFilterMixin, 
    RiscoListView
):
    template_name = 'prontuario/risco/risco_list.html'

    
class RiscoProntuarioCreateView(
    LoginRequiredMixin, 
    AdolescenteFormBindMixin,
    RiscoCreateView
):
    template_name = "prontuario/risco/risco_form.html"
    
    def get_success_url(self):
        return reverse('prontuario:risco-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})
    
class RiscoProntuarioUpdateView(
    LoginRequiredMixin, 
    RiscoUpdateView
):
    template_name = "prontuario/risco/risco_form.html"
    
    def get_success_url(self):
        return reverse('prontuario:risco-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})

