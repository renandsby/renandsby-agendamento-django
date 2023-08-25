import django_filters
from django.db.models import Q

from .models import Endereco
# from posicao.models import Posicao




# class PosicaoFilterSet(django_filters.FilterSet):
#     @property
#     def qs(self):
#         parent_qs = super(PosicaoFilterSet, self).qs
        # print('->>>>>', parent_qs)
        # # OBRIGA o filtro de bairro
        # if 'bairro' in self.request.GET:
        #     if self.request.GET['bairro']:
        #         return parent_qs
    #     print(parent_qs)
    #     return parent_qs

    # class Meta:
    #     model = Endereco
        # fields = ("tipo_rede_localizacao", "bairro")