from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from atendimento_psicossocial.views import (
    AtendimentoPsicossocialCreateView,
    AtendimentoPsicossocialListView,
    AtendimentoPsicossocialUpdateView
)

from .prontuario_base import (
    AdolescenteFilterMixin, 
    AdolescenteFormBindMixin
)



class AtendimentoPsicossocialProntuarioListView(
    LoginRequiredMixin, 
    AdolescenteFilterMixin,
    AtendimentoPsicossocialListView
):
    template_name = "prontuario/atendimento_psicossocial/atendimento_psicossocial_list.html"


class AtendimentoPsicossocialProntuarioCreateView(
    LoginRequiredMixin,
    AdolescenteFormBindMixin,
    AtendimentoPsicossocialCreateView
):
    template_name = "prontuario/atendimento_psicossocial/atendimento_psicossocial_form.html"

    def get_success_url(self):
        return reverse("prontuario:atendimento-psicossocial-list", kwargs={"adolescente_uuid":self.kwargs["adolescente_uuid"]})

class AtendimentoPsicossocialProntuarioUpdateView(
    LoginRequiredMixin,
    AtendimentoPsicossocialUpdateView
):
    template_name = "prontuario/atendimento_psicossocial/atendimento_psicossocial_form.html"

    def get_success_url(self):
        return reverse("prontuario:atendimento-psicossocial-list", kwargs={"adolescente_uuid":self.kwargs["adolescente_uuid"]})
