from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .prontuario_base import (
    AdolescenteFilterMixin, 
    AdolescenteFormBindMixin
)

from adolescentes.views import (
    EnderecoCreateView,
    EnderecoListView,
    EnderecoUpdateView
)



class EnderecoProntuarioListView(
    LoginRequiredMixin, 
    AdolescenteFilterMixin,
    EnderecoListView
):
    template_name = 'prontuario/endereco/endereco_list.html'
    
    
class EnderecoProntuarioCreateView(
    LoginRequiredMixin,
    AdolescenteFormBindMixin,
    EnderecoCreateView
):
    template_name = "prontuario/endereco/endereco_form.html"

    def get_success_url(self):
        return reverse('prontuario:endereco-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})


class EnderecoProntuarioUpdateView(
    LoginRequiredMixin, 
    EnderecoUpdateView
):
    template_name = "prontuario/endereco/endereco_form.html"
    
    def get_success_url(self):
        return reverse('prontuario:endereco-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})