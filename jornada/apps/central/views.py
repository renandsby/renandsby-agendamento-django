from django.urls.base import reverse
from core.permission_mixins import CustomPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from alteracoes_vinculo.views import (
    VinculacaoCreateView,
    VinculacaoListView,
    VinculacaoUpdateView,
    VinculacaoDeleteView,
    VinculacaoCancelarView,
    VinculacaoDesfazerView,
    VincularView,

    TransferenciaCreateView,
    TransferenciaListView,
    TransferenciaUpdateView,
    TransferenciaDeleteView,
    TransferenciaCancelarView,
    TransferenciaDesfazerView,
    TransferirView,

    DesvinculacaoCreateView,
    DesvinculacaoListView,
    DesvinculacaoUpdateView,
    DesvinculacaoDeleteView,
    DesvinculacaoCancelarView,
    DesvinculacaoDesfazerView,
    DesvincularView,
)

from solicitacoes.forms import SolicitacaoCentralForm
from solicitacoes.views import (
    SolicitacaoListView,
    SolicitacaoUpdateView,
    SolicitacaoDeleteView
)


### SOLICITAÇÃO
class SolicitacaoCentralListView(
    CustomPermissionMixin,
    LoginRequiredMixin,  
    SolicitacaoListView
):
    permission_required = ['solicitacoes.ver']
    template_name = "central/solicitacoes/solicitacao_list.html"

class SolicitacaoCentralUpdateView(
    CustomPermissionMixin,
    LoginRequiredMixin,
    SolicitacaoUpdateView
):
    permission_required = ['solicitacoes.editar']
    check_permission_only_in_post = True
    template_name = "central/solicitacoes/solicitacao_form.html"
    form_class = SolicitacaoCentralForm

    def get_success_url(self):
        return reverse('central:solicitacao-list')
    

class SolicitacaoCentralDeleteView(
    CustomPermissionMixin,
    LoginRequiredMixin,
    SolicitacaoDeleteView
):
    permission_required = ['solicitacoes.excluir']
    def get_success_url(self):
        return reverse('central:solicitacao-list')




### VINCULAÇÃO

class VinculacaoCentralListView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    VinculacaoListView
):
    permission_required = ['alteracoes_vinculo.ver_vinculacoes']
    template_name = "central/vinculacoes/vinculacao_list.html"

class VinculacaoCentralCreateView(
    CustomPermissionMixin,
    LoginRequiredMixin,
    VinculacaoCreateView
):
    template_name = "central/vinculacoes/vinculacao_form.html"
    permission_required = ['alteracoes_vinculo.criar_vinculacoes']
    
    def get_success_url(self):
        return reverse('central:vinculacao-list')
    
    
  
class VinculacaoCentralUpdateView(
    CustomPermissionMixin,
    LoginRequiredMixin,
    VinculacaoUpdateView
):
    template_name = "central/vinculacoes/vinculacao_form.html"
    permission_required = ['alteracoes_vinculo.editar_vinculacoes']
    check_permission_only_in_post = True

    def get_success_url(self):
        return reverse('central:vinculacao-list')
    
  
class VinculacaoCentralDeleteView(
    CustomPermissionMixin,
    LoginRequiredMixin,
    VinculacaoDeleteView
):
    permission_required = ['alteracoes_vinculo.deletar_vinculacoes']
    
    def get_success_url(self):
        return reverse('central:vinculacao-list')


class VincularCentralView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    VincularView
):
    permission_required = ['alteracoes_vinculo.editar_vinculacoes']
    def get_success_url(self):
        return reverse('central:vinculacao-list')


class VinculacaoCentralDesfazerView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    VinculacaoDesfazerView
):
    permission_required = ['alteracoes_vinculo.editar_vinculacoes']
    def get_success_url(self):
        return reverse('central:vinculacao-list')


class VinculacaoCentralCancelarView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    VinculacaoCancelarView
):
    permission_required = ['alteracoes_vinculo.editar_vinculacoes']
    def get_success_url(self):
        return reverse('central:vinculacao-list')






### TRANSFERÊNCIA


class TransferenciaCentralListView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    TransferenciaListView
):
    permission_required = ['alteracoes_vinculo.ver_transferencias']
    template_name = "central/transferencias/transferencia_list.html"
    

class TransferenciaCentralCreateView(
    CustomPermissionMixin,
    LoginRequiredMixin,
    TransferenciaCreateView
):
    permission_required = ['alteracoes_vinculo.criar_transferencias']
    template_name = "central/transferencias/transferencia_form.html"

    def get_success_url(self):
        return reverse('central:transferencia-list')
    
  
class TransferenciaCentralUpdateView(
    CustomPermissionMixin,
    LoginRequiredMixin,
    TransferenciaUpdateView
):
    permission_required = ['alteracoes_vinculo.editar_transferencias']
    check_permission_only_in_post = True
    template_name = "central/transferencias/transferencia_form.html"
    
    def get_success_url(self):
        return reverse('central:transferencia-list')
    
  
class TransferenciaCentralDeleteView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    TransferenciaDeleteView
):  
    permission_required = ['alteracoes_vinculo.deletar_transferencias']
    def get_success_url(self):
        return reverse('central:transferencia-list')
    
class TransferirCentralView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    TransferirView
):
    permission_required = ['alteracoes_vinculo.editar_transferencias']
    def get_success_url(self):
        return reverse('central:transferencia-list')


class TransferenciaCentralDesfazerView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    TransferenciaDesfazerView
):
    permission_required = ['alteracoes_vinculo.editar_transferencias']
    def get_success_url(self):
        return reverse('central:transferencia-list')


class TransferenciaCentralCancelarView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    TransferenciaCancelarView
):
    permission_required = ['alteracoes_vinculo.editar_transferencias']
    def get_success_url(self):
        return reverse('central:transferencia-list')




### DESVINCULAÇÃO


class DesvinculacaoCentralListView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    DesvinculacaoListView
):
    permission_required = ['alteracoes_vinculo.ver_desvinculacoes']
    template_name = "central/desvinculacoes/desvinculacao_list.html"
    

class DesvinculacaoCentralCreateView(
    CustomPermissionMixin,
    LoginRequiredMixin,
    DesvinculacaoCreateView
):
    permission_required = ['alteracoes_vinculo.criar_desvinculacoes']
    template_name = "central/desvinculacoes/desvinculacao_form.html"

    def get_success_url(self):
        return reverse('central:desvinculacao-list')
    
  
class DesvinculacaoCentralUpdateView(
    CustomPermissionMixin,
    LoginRequiredMixin,
    DesvinculacaoUpdateView
):
    permission_required = ['alteracoes_vinculo.editar_desvinculacoes']
    check_permission_only_in_post = True
    template_name = "central/desvinculacoes/desvinculacao_form.html"
  
    def get_success_url(self):
        return reverse('central:desvinculacao-list')
    
  
class DesvinculacaoCentralDeleteView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    DesvinculacaoDeleteView
):
    permission_required = ['alteracoes_vinculo.deletar_desvinculacoes']
    def get_success_url(self):
        return reverse('central:desvinculacao-list')


class DesvincularCentralView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    DesvincularView
):
    permission_required = ['alteracoes_vinculo.editar_desvinculacoes']
    def get_success_url(self):
        return reverse('central:desvinculacao-list')


class DesvinculacaoCentralDesfazerView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    DesvinculacaoDesfazerView
):
    permission_required = ['alteracoes_vinculo.editar_desvinculacoes']
    def get_success_url(self):
        return reverse('central:desvinculacao-list')


class DesvinculacaoCentralCancelarView(
    CustomPermissionMixin,
    LoginRequiredMixin, 
    DesvinculacaoCancelarView
):
    permission_required = ['alteracoes_vinculo.editar_desvinculacoes']
    def get_success_url(self):
        return reverse('central:desvinculacao-list')


