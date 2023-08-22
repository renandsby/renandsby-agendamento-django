from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .prontuario_base import (
    AdolescenteFilterMixin, 
    AdolescenteFormBindMixin
)

from educacao.views import (
    EducacaoCreateView,
    EducacaoListView,
    EducacaoUpdateView
)



class EducacaoProntuarioListView(
    LoginRequiredMixin, 
    AdolescenteFilterMixin,
    EducacaoListView
):
    template_name = 'prontuario/educacao/educacao_list.html'
    
    
class EducacaoProntuarioCreateView(
    LoginRequiredMixin,
    AdolescenteFormBindMixin,
    EducacaoCreateView
):
    template_name = "prontuario/educacao/educacao_form.html"

    def get_success_url(self):
        return reverse('prontuario:educacao-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})


class EducacaoProntuarioUpdateView(
    LoginRequiredMixin, 
    EducacaoUpdateView
):
    template_name = "prontuario/educacao/educacao_form.html"
    
    def get_success_url(self):
        return reverse('prontuario:educacao-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})