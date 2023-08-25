import glob

from posicao.views import ( PosicaoCreateView,
                                PosicaoListView, PosicaoUpdateView)

from .dadosEmpresa_base import (
    RedeEmpresasFilterMixin,
    RedeEmpresasFormBindMixin
)

from core.permission_mixins import CustomPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django_weasyprint import WeasyTemplateResponseMixin


class RedeDadosEmpresaListView(
     PosicaoListView
):
    template_name = "dadosEmpresa/posicao/rede_list.html"


class RedeDadosEmpresaCreateView( PosicaoCreateView):
    template_name = "dadosEmpresa/posicao/rede_form.html"

    def get_success_url(self):
        return reverse(
            "dadosEmpresa:rede-update",
            kwargs={"rede": self.object.uuid},
        )


class RedeDadosEmpresaUpdateView(PosicaoUpdateView):
    template_name = "dadosEmpresa/posicao/rede_form.html"
    
    def get_success_url(self):
        return reverse(
            "dadosEmpresa:rede-update",
            kwargs={"rede": self.object.uuid},
        )


