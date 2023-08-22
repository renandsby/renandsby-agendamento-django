import django_filters
from django.db.models import Q
from .models import UnidadeDeApoio
from unidades.models import Unidade


class RedeDeApoioFilterSet(django_filters.FilterSet):
    @property
    def qs(self):
        parent_qs = super(RedeDeApoioFilterSet, self).qs

        # OBRIGA o filtro de bairro
        if 'bairro' in self.request.GET:
            if self.request.GET['bairro']:
                return parent_qs

        return UnidadeDeApoio.objects.none()

    class Meta:
        model = UnidadeDeApoio
        fields = ("tipo_rede_apoio", "bairro")