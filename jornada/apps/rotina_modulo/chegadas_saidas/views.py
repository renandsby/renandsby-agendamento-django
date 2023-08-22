from atividades.forms import AdolescenteAtividadeFormset
from core.exceptions import get_error_message
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.views import View
from unidades.forms import EditaEntradaAdmUnidadeForm
from unidades.views import (
    AcautelamentoListView, 
    AcautelamentoUpdateView,
    EntradaAdolescenteLotadosListView,
    EntradaUpdateView, 
    SaidaListView, 
    SaidaView
)
from unidades.filters import EfetivoGeralFilterSet
from core.views import FilteredViewMixin

class AdministradorAcautelamentoListView(LoginRequiredMixin, AcautelamentoListView):
    template_name = "rotina_modulo/chegadas_saidas/acautelamento-list.html"

    def get_queryset(self, **kwargs):
        return (
            super().get_queryset().filter(unidade__uuid=self.kwargs.get("unidade_uuid"))
        )


class AdministradorAcautelamentoUpdateView(LoginRequiredMixin, AcautelamentoUpdateView):
    template_name = "rotina_modulo/chegadas_saidas/acautelamento-form.html"

    def get_success_url(self):
        return reverse(
            "rotina_modulo:acautelamento-list",
            kwargs={"unidade_uuid": self.kwargs.get("unidade_uuid")},
        )

    def form_valid(self, form):
        try:
            return_value = super().form_valid(form)
        except Exception as e:
            messages.error(
                self.request,
                f"O adolescente {self.object.adolescente} não pôde ser acautelado(a). {get_error_message(e)}",
            )
            return redirect(self.get_success_url())
        else:
            messages.success(
                self.request, f"{self.object.adolescente} acautelado(a) com sucesso."
            )
        return return_value


class AdministradorSaidaListView(LoginRequiredMixin, SaidaListView):
    template_name = "rotina_modulo/chegadas_saidas/saida-list.html"

    def get_queryset(self, **kwargs):
        return (
            super()
            .get_queryset()
            .filter(unidade__uuid=self.kwargs.get("unidade_uuid"), status=3)
        )


class AdministradorSaidaView(LoginRequiredMixin, SaidaView):
    template_name = "rotina_modulo/chegadas_saidas/saida-form.html"

    def form_valid(self, form):
        try:
            return_value = super().form_valid(form)
        except Exception as e:
            messages.error(
                self.request,
                f"Não foi possível realizar a Saída do adolescente {self.object.adolescente}. {get_error_message(e)}",
            )
            return redirect(self.get_success_url())
        else:
            messages.success(
                self.request,
                f"Saida de {self.object.adolescente} realizado com sucesso.",
            )
        return return_value

    def get_success_url(self):
        return reverse(
            "rotina_modulo:saida-list",
            kwargs={"unidade_uuid": self.object.unidade.uuid},
        )


class EfetivoGeralListView(
    LoginRequiredMixin, 
    FilteredViewMixin,
    EntradaAdolescenteLotadosListView
):
    template_name = "rotina_modulo/efetivo_geral/efetivo-list.html"
    filterset_class = EfetivoGeralFilterSet

    def get_queryset(self, **kwargs):
        return (
            super()
            .get_queryset(**kwargs)
            .filter(unidade__uuid=self.kwargs.get("unidade_uuid"))
            .order_by("modulo", "quarto", "adolescente__nome")
        )


class AdministradorEntradaUpdateView(LoginRequiredMixin, EntradaUpdateView):
    template_name = "rotina_modulo/efetivo_geral/efetivo-edita-entrada-form.html"
    form_class = EditaEntradaAdmUnidadeForm
    def get_success_url(self):
        return reverse(
            "rotina_modulo:efetivo-geral-list",
            kwargs={"unidade_uuid": self.object.unidade.uuid},
        )
