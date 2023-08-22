import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin
from core.filters import PlantaoFilter
from core.forms.mixins import InlineFormsetMixin
from core.views import FilteredViewMixin, UUIDViewMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from unidades.models import Modulo, Unidade
from django_weasyprint import WeasyTemplateResponseMixin
import glob
from .forms import (AcompanhamentoLivroFormeSet, LivroForm,NovoPlantaoForm)
from .models import Acompanhamento, Livro




class LivroReportView(
    LoginRequiredMixin,
    WeasyTemplateResponseMixin,
    UUIDViewMixin,
    DetailView,
):
    model = Livro
    context_object_name = "livro"
    uuid_url_kwarg = "livro_uuid"
    template_name = "livro/livro_report.html"
    pdf_attachment = False
    pdf_stylesheets = glob.glob("static/css/bootstrap/*.css")
    pdf_filename = "livro.pdf"
    

class LivroRedirectView(View):
    def get(self, request, *args, **kwargs):
        if self.kwargs.get("modulo_uuid"):
            modulo_livro = Modulo.objects.get(uuid=self.kwargs.get("modulo_uuid"))
            ultimo_registro_modulo = modulo_livro.ultimo_livro
            if ultimo_registro_modulo:
                return redirect(
                    "rotina_modulo:livro-update",
                    modulo_uuid=self.kwargs["modulo_uuid"],
                    livro_uuid=ultimo_registro_modulo.uuid,
                )
            return redirect(
                "rotina_modulo:livro-create",
                modulo_uuid=self.kwargs["modulo_uuid"],
            )

        if self.kwargs.get("unidade_uuid"):
            unidade_livro = Unidade.objects.get(uuid=self.kwargs.get("unidade_uuid"))
            ultimo_registro_unidade = unidade_livro.ultimo_livro
            if ultimo_registro_unidade:
                return redirect(
                    "rotina_modulo:livro-c2-update",
                    unidade_uuid=self.kwargs["unidade_uuid"],
                    livro_uuid=ultimo_registro_unidade.uuid,
                )
            return redirect(
                "rotina_modulo:livro-c2-create",
                unidade_uuid=self.kwargs["unidade_uuid"],
            )


class LivroPassagemPlantaoView(CreateView):
    model = Livro
    form_class = NovoPlantaoForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        if "modulo_uuid" in self.kwargs:
            kwargs["modulo"] = Modulo.objects.get(uuid=self.kwargs.get("modulo_uuid"))
        if "unidade_uuid" in self.kwargs:
            kwargs["unidade"] = Unidade.objects.get(uuid=self.kwargs.get("unidade_uuid"))
        return kwargs

    def form_valid(self, form):
        if "modulo_uuid" in self.kwargs:
            form.instance.modulo = Modulo.objects.get(uuid=self.kwargs.get("modulo_uuid"))
        if "unidade_uuid" in self.kwargs:
            form.instance.unidade = Unidade.objects.get(uuid=self.kwargs.get("unidade_uuid"))
        return super().form_valid(form)


class LivroUpdateView(InlineFormsetMixin, UUIDViewMixin, UpdateView):
    model = Livro
    form_class = LivroForm
    uuid_url_kwarg = "livro_uuid"
    inlineformset_classes = {"acompanhamentos": AcompanhamentoLivroFormeSet}

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        if "modulo_uuid" in self.kwargs:
            kwargs["modulo"] = Modulo.objects.get(uuid=self.kwargs.get("modulo_uuid"))
        if "unidade_uuid" in self.kwargs:
            kwargs["unidade"] = Unidade.objects.get(uuid=self.kwargs.get("unidade_uuid"))
        return kwargs

    def form_valid(self, form):
        if "modulo_uuid" in self.kwargs:
            form.instance.modulo = Modulo.objects.get(
                uuid=self.kwargs.get("modulo_uuid")
            )
        if "unidade_uuid" in self.kwargs:
            form.instance.unidade = Unidade.objects.get(
                uuid=self.kwargs.get("unidade_uuid")
            )
        return super().form_valid(form)
