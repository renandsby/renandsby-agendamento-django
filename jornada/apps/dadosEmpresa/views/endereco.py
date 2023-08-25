from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .dadosEmpresa_base import (
    RedeEmpresasFilterMixin,
    RedeEmpresasFormBindMixin
)

from posicao.views import (
    EnderecoCreateView,
    EnderecoListView,
    EnderecoUpdateView
)



class EnderecoDadosEmpresaListView(
    LoginRequiredMixin, 
    RedeEmpresasFilterMixin,
    EnderecoListView
):
    template_name = 'dadosEmpresa/endereco/endereco_list.html'
    
    
class EnderecoDadosEmpresaCreateView(
    LoginRequiredMixin,
    RedeEmpresasFormBindMixin,
    EnderecoCreateView
):
    template_name = "dadosEmpresa/endereco/endereco_form.html"

    def get_success_url(self):
        return reverse('dadosEmpresa:endereco-list', kwargs={"rede_uuid": self.kwargs.get("rede_uuid")})


class EnderecoDadosEmpresaUpdateView(
    LoginRequiredMixin, 
    EnderecoUpdateView
):
    template_name = "dadosEmpresa/endereco/endereco_form.html"
    
    def get_success_url(self):
        return reverse('dadosEmpresa:endereco-list', kwargs={"rede_uuid": self.kwargs.get("rede_uuid")})