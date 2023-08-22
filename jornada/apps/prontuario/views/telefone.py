import glob

from adolescentes.models import Adolescente
from adolescentes.views import (TelefoneCreateView, TelefoneListView,
                                TelefoneUpdateView)
from core.views import UUIDViewMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin

from .prontuario_base import AdolescenteFilterMixin, AdolescenteFormBindMixin


class TelefoneProntuarioListView(
    LoginRequiredMixin, AdolescenteFilterMixin, TelefoneListView
):
    template_name = "prontuario/telefone/telefone_list.html"


class TelefoneProntuarioCreateView(
    LoginRequiredMixin, AdolescenteFormBindMixin, TelefoneCreateView
):
    template_name = "prontuario/telefone/telefone_form.html"

    def get_success_url(self):
        return reverse(
            "prontuario:telefone-list",
            kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")},
        )


class TelefoneProntuarioUpdateView(LoginRequiredMixin, TelefoneUpdateView):
    template_name = "prontuario/telefone/telefone_form.html"

    def get_success_url(self):
        return reverse(
            "prontuario:telefone-list",
            kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")},
        )


class TelefoneReportView(
    LoginRequiredMixin,
    WeasyTemplateResponseMixin,
    UUIDViewMixin,
    DetailView,
):
    model = Adolescente
    context_object_name = "adolescente"
    uuid_url_kwarg = "adolescente_uuid"
    template_name = "prontuario/telefone/telefones_autorizados_report.html"
    pdf_attachment = False
    pdf_stylesheets = glob.glob("static/css/bootstrap/*.css")
    pdf_filename = "telefone.pdf"
