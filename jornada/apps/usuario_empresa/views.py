from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView,
)

from core.views import UUIDViewMixin, FilteredViewMixin
from core.forms.mixins import InlineFormsetMixin
from django.db.models import F, Func, Value, Q, When, Case
from django.db.models.functions import Cast
from django.db.models import IntegerField, CharField
from .models import UsuarioEmpresa
from django.urls.base import reverse


from .forms import (
    UsuarioEmpresaForm
   
)

from core.permission_mixins import CustomPermissionMixin


class UsuarioEmpresaListView(CustomPermissionMixin, ListView):
    model = UsuarioEmpresa
    template_name = "usuario_empresa/usuario_list.html"
    # permission_required = ["unidades.acessar_todas"]
    # no_permission_redirect_url = "/"

class UsuarioEmpresaCreateView(CreateView):
    model = UsuarioEmpresa
    form_class = UsuarioEmpresaForm
    template_name ="usuario_empresa/usuario_form.html"
    def get_success_url(self):
        return reverse('usuario_empresa:usuario-create')
    # permission_required = ["unidades.incluir_unidades"]
    # no_permission_redirect_url = "/"


class UsuarioEmpresaUpdateView(
    UUIDViewMixin,
    CustomPermissionMixin,
    UpdateView
):
    model = UsuarioEmpresa
    form_class = UsuarioEmpresaForm
    uuid_url_kwarg = "usuario_empresa_uuid"
    template_name = "usuario_empresa/usuario_form.html"
    # permission_required = ["usuario_empresa_uuid.editar_unidades"]
    # no_permission_redirect_url = "/"


class ExtractInteger(Func):
    """ Returns the first int value from the string. Note that this
    requires the string to have an integer value inside.
    """
    function = 'REGEXP_MATCH'
    template = "CAST( (%(function)s(%(expressions)s, '\d+'))[1] as INTEGER )"
    output_field = IntegerField()
