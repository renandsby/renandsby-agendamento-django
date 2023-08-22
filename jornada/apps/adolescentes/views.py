from django.views.generic import ListView, CreateView, UpdateView, DetailView, detail
from django.urls.base import reverse
from adolescentes.models import Adolescente, Endereco, Relatorio
from core.forms.mixins import InlineFormsetMixin
from core.permission_mixins import CustomPermissionMixin
from core.views import FilteredViewMixin, UUIDViewMixin
from django.http import HttpResponse
from .filters import AdolescenteFilterSet
from .forms import (
    AdolescenteCreateForm,
    EnderecoForm,
    FamiliarForm,
    TelefoneForm,
    RelatorioForm,
    FotoAdolescenteFormSet,
    TelefoneAdolescenteFormSet,
    FamiliarAdolescenteFormSet,
    AnexoFamiliarFormSet,
    AnexoTelefoneFormSet,
    DocumentoAnexoFormSet,
    AnexoEnderecoFormSet,
    ObservacoesFormSet,
    DocumentoAnexo,
    Telefone,
    Relatorio,
    Familiar,
    Endereco,
    Foto,
)


class AdolescenteListView(FilteredViewMixin, ListView):
    template_name = ""
    paginate_by = 30
    filterset_class = AdolescenteFilterSet
    model = Adolescente
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("nome")


class AdolescenteCreateView(
    InlineFormsetMixin, 
    CustomPermissionMixin, 
    CreateView
):
    model = Adolescente
    form_class = AdolescenteCreateForm
    template_name = ""
    inlineformset_classes = {
        "fotos": FotoAdolescenteFormSet,
        "documentos_anexados": DocumentoAnexoFormSet,
    }
    permission_required = ["adolescentes.incluir"]

    def get_no_permission_redirect_url(self):
        return reverse("prontuario:adolescente-list")


class AdolescenteUpdateView(
    InlineFormsetMixin,
    UUIDViewMixin,
    UpdateView,
):
    model = Adolescente
    fields = "__all__"
    template_name = ""
    inlineformset_classes = {
        "fotos": FotoAdolescenteFormSet,
        "documentos_anexados": DocumentoAnexoFormSet,
    }
    uuid_url_kwarg = "adolescente_uuid"


class AdolescenteDetailView(
    InlineFormsetMixin,
    UUIDViewMixin,
    DetailView,
):
    model = Adolescente
    fields = "__all__"
    template_name = ""
    inlineformset_classes = {
        "telefones": TelefoneAdolescenteFormSet,
        "familiares": FamiliarAdolescenteFormSet,
        "fotos": FotoAdolescenteFormSet,
        "documentos_anexados": DocumentoAnexoFormSet,
    }
    uuid_url_kwarg = "adolescente_uuid"


class EnderecoListView(ListView):
    template_name = ""
    model = Endereco

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-reside', 'id')

class EnderecoCreateView(
    InlineFormsetMixin,
    CreateView
    ):
    model = Endereco
    form_class = EnderecoForm
    inlineformset_classes = {
        "anexos": AnexoEnderecoFormSet,
    }
    template_name = ""

class EnderecoUpdateView(
    UUIDViewMixin, 
    InlineFormsetMixin,
    UpdateView
):
    model = Endereco
    form_class = EnderecoForm
    inlineformset_classes = {
        "anexos": AnexoEnderecoFormSet,
    }
    template_name = ""
    uuid_url_kwarg = "endereco_uuid"
    

class FamiliarListView(ListView):
    template_name = ""
    model = Familiar

class FamiliarCreateView(
    InlineFormsetMixin,
    CreateView
):
    model = Familiar
    form_class = FamiliarForm
    inlineformset_classes = {
        "anexos": AnexoFamiliarFormSet,
    }
    template_name = ""

class FamiliarUpdateView(
    UUIDViewMixin, 
    InlineFormsetMixin,
    UpdateView
):
    model = Familiar
    form_class = FamiliarForm
    inlineformset_classes = {
        "anexos": AnexoFamiliarFormSet,
    }
    uuid_url_kwarg = "familiar_uuid"
    template_name = ""
    

class TelefoneListView(ListView):
    template_name = ""
    model = Telefone

class TelefoneCreateView(
    InlineFormsetMixin,
    CreateView
):
    model = Telefone
    form_class = TelefoneForm
    template_name = ""
    inlineformset_classes = {
        "anexos": AnexoTelefoneFormSet,
    }

class TelefoneUpdateView(
    UUIDViewMixin, 
    InlineFormsetMixin,
    UpdateView
):
    model = Telefone
    form_class = TelefoneForm
    template_name = ""
    uuid_url_kwarg = "telefone_uuid"
    inlineformset_classes = {
        "anexos": AnexoTelefoneFormSet,
    }

class RelatorioListView(ListView):
    template_name = ""
    model = Relatorio

class RelatorioCreateView(
    CreateView
):
    model = Relatorio
    form_class = RelatorioForm
    template_name = ""

class RelatorioUpdateView(
    UUIDViewMixin, 
    UpdateView
):
    model = Relatorio
    form_class = RelatorioForm
    template_name = ""
    uuid_url_kwarg = "relatorio_uuid"

