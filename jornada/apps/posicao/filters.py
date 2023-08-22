import django_filters
from django.db.models import Q

from .models import RedeDeLocalizacao
# from posicao.models import Posicao




class PosicaoFilterSet(django_filters.FilterSet):
    @property
    def qs(self):
        parent_qs = super(PosicaoFilterSet, self).qs

        # OBRIGA o filtro de bairro
        if 'bairro' in self.request.GET:
            if self.request.GET['bairro']:
                return parent_qs

        return RedeDeLocalizacao.objects.all()

    class Meta:
        model = RedeDeLocalizacao
        fields = ("tipo_rede_localizacao", "bairro")