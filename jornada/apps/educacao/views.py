from core.forms.mixins import InlineFormsetMixin
from core.views import UUIDViewMixin
from django.views.generic import CreateView, ListView, UpdateView

from .forms import AnexoEducacaoFormSet, EducacaoForm
from .models import AtendimentoEducacao


class EducacaoListView(ListView):
    model = AtendimentoEducacao
    template_name = ""


class EducacaoCreateView(InlineFormsetMixin, CreateView):
    model = AtendimentoEducacao
    form_class = EducacaoForm
    template_name = ""
    inlineformset_classes = {"anexos": AnexoEducacaoFormSet}


class EducacaoUpdateView(InlineFormsetMixin, UUIDViewMixin, UpdateView):
    model = AtendimentoEducacao
    form_class = EducacaoForm
    uuid_url_kwarg = "edu_uuid"
    template_name = ""
    inlineformset_classes = {"anexos": AnexoEducacaoFormSet}
