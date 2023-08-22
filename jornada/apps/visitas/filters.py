import django_filters
from adolescentes.models import Adolescente
from django_filters.widgets import BooleanWidget
from unidades.models import Modulo
from django.utils.translation import gettext as _
from core.filters import DateRangeFilter



def OpcoesAdolescente(request):
    if request is None:
        return Adolescente.objects.none()
    
    if 'modulo_uuid' in request.resolver_match.kwargs:    
        modulo = Modulo.objects.get(uuid=request.resolver_match.kwargs.get('modulo_uuid'))
        return Adolescente.objects.filter(id__in=modulo.ids_adolescentes_lotados)

    return Adolescente.objects.none()



class CustomBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("", _("Todos")), ("true", _("Em Visita")), ("false", _("Visita Finalizada")))
        self.attrs['class'] = self.attrs.get('class', "") + ' form-select'
        
class VisitaFilterset(django_filters.FilterSet):
    adolescente = django_filters.ModelChoiceFilter(label="Adolescente", queryset=OpcoesAdolescente, empty_label="Todos")
    periodo = DateRangeFilter(empty_label="Todos", label="Período", field_name="data_entrada")
    em_visita = django_filters.BooleanFilter(label="Situação", widget=CustomBooleanWidget)