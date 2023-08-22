import glob

from adolescentes.views import (AdolescenteCreateView, AdolescenteDetailView,
                                AdolescenteListView, AdolescenteUpdateView)
from core.permission_mixins import CustomPermissionMixin, FiltraAdolescentes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django_weasyprint import WeasyTemplateResponseMixin


class AdolescenteProntuarioListView(
    LoginRequiredMixin, FiltraAdolescentes, AdolescenteListView
):
    template_name = "prontuario/adolescente/adolescente_list.html"


class AdolescenteProntuarioCreateView(LoginRequiredMixin, AdolescenteCreateView):
    template_name = "prontuario/adolescente/adolescente_form.html"

    def get_success_url(self):
        return reverse(
            "prontuario:adolescente-update",
            kwargs={"adolescente_uuid": self.object.uuid},
        )


class AdolescenteProntuarioUpdateView(LoginRequiredMixin, AdolescenteUpdateView):
    template_name = "prontuario/adolescente/adolescente_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if (    
                hasattr(self.request.user, 'servidor') and 
                self.request.user.servidor is not None and 
                self.request.user.servidor.unidade is not None
            ):
            context['passagens_unidade_usuario'] = self.object.entradas_em_unidades.filter(unidade=self.request.user.servidor.unidade).count()
        return context
    
    def get_success_url(self):
        return reverse(
            "prontuario:adolescente-update",
            kwargs={"adolescente_uuid": self.object.uuid},
        )


class AdolescenteProntuarioDetailView(
    LoginRequiredMixin,
    # AdolescenteDetailView
    AdolescenteUpdateView,
):
    template_name = "prontuario/adolescente/adolescente_detail.html"

    def get_success_url(self):
        return reverse(
            "prontuario:adolescente-update",
            kwargs={"adolescente_uuid": self.object.uuid},
        )


class AdolescenteProntuarioToPrintDetailView(
    LoginRequiredMixin,
    WeasyTemplateResponseMixin,
    AdolescenteDetailView,
):
    template_name = "prontuario/adolescente/adolescente_detail_to_print.html"
    pdf_attachment = False
    pdf_stylesheets = glob.glob("static/css/bootstrap/*.css")
    pdf_filename = "prontuario.pdf"

    def get_success_url(self):
        return reverse(
            "prontuario:adolescente-update",
            kwargs={"adolescente_uuid": self.object.uuid},
        )
