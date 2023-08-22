from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView
from core.forms.mixins import InlineFormsetMixin
from django.urls.base import reverse
from core.views import FilteredViewMixin, UUIDViewMixin
from core.permission_mixins import CustomPermissionMixin
from core.exceptions import ValidationError
from .forms import (
    AnexoAtendimentoFormSet, 
    AtendimentoPsicossocialForm,
)
from .models import AtendimentoPsicossocial
from .filters import AtendimentoPsicossocialFilterSet



class AtendimentoPsicossocialListView(
    FilteredViewMixin,
    ListView
):
    model = AtendimentoPsicossocial
    filterset_class = AtendimentoPsicossocialFilterSet
    paginate_by = 10
    template_name = ""
    
    def get_no_permission_redirect_url(self):
        return reverse("prontuario:adolescente-update", kwargs={"adolescente_uuid":self.kwargs["adolescente_uuid"]})
    


class AtendimentoPsicossocialCreateView(
    InlineFormsetMixin,
    CustomPermissionMixin,
    CreateView
):
    model = AtendimentoPsicossocial
    form_class = AtendimentoPsicossocialForm
    inlineformset_classes = {
        "anexos" : AnexoAtendimentoFormSet
    }
    template_name = ""
    permission_required = ["atendimento_psicossocial.incluir"]
    def get_no_permission_redirect_url(self):
        return reverse("prontuario:atendimento-psicossocial-list", kwargs={"adolescente_uuid":self.kwargs["adolescente_uuid"]})
    


class AtendimentoPsicossocialUpdateView(
    InlineFormsetMixin,
    UUIDViewMixin,
    CustomPermissionMixin,
    UpdateView
):
    model = AtendimentoPsicossocial
    form_class = AtendimentoPsicossocialForm
    uuid_url_kwarg = "atend_uuid"
    inlineformset_classes = {
        "anexos" : AnexoAtendimentoFormSet
    }
    template_name = ""
    permission_required = ["atendimento_psicossocial.ver"]
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        form = self.get_form()
        if form.instance.updating:
            if form.instance.criado_por != self.request.user:
                from django.contrib import messages
                from django.shortcuts import redirect
                
                messages.error(self.request, f'Apenas o criador do atendimento pode editá-lo.')
                
                referer = self.request.META.get('HTTP_REFERER')
                redirect_url = referer if referer is not None else self.get_success_url()
                return redirect(redirect_url)
                
            
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
        
    
    def get_no_permission_redirect_url(self):
        return reverse("prontuario:atendimento-psicossocial-list", kwargs={"adolescente_uuid":self.kwargs["adolescente_uuid"]})
    
