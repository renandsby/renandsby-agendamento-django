from typing import Any, Dict
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile,TemporaryUploadedFile

from core.views import FilteredViewMixin, UUIDViewMixin
from core.forms.mixins import InlineFormsetMixin
from core.exceptions import get_error_message

from unidades.models import EntradaAdolescente, Modulo, Unidade
from adolescentes.models import Adolescente

from .models import Atividade, HistoricoAtividade, AnexoHistoricoAtividade
from .filters import AtividadeFilterSet, AgendamentoFilterset, HistoricoFilterset
from .forms import (
    AgendamentoForm,
    AgendamentoRetornarForm,
    AtividadeForm, 
    AdolescenteAtividadeFormset, 
    EnvioAdolescentesForm, 
    RetornoAdolescentesForm,
    AgendamentoAtividadeForm,
    AgendamentoEnviarForm,
    AnexoAgendamentoAtividadeFormset,
    HistoricoAtividadeForm
)



class AtividadeListView(
    FilteredViewMixin, 
    ListView
):
    '''
    Lista as Atividades cadastradas na Unidade
    '''
    model = Atividade
    paginate_by = 20
    filterset_class = AtividadeFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(unidade__uuid=self.kwargs['unidade_uuid'])
        


class AtividadeCreateView(CreateView):
    '''
    Cria uma Atividade nova em uma Unidade
    '''
    model = Atividade
    form_class = AtividadeForm

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs =  super().get_form_kwargs()
        if 'unidade_uuid' in self.kwargs:
            kwargs['unidade'] = Unidade.objects.get(uuid=self.kwargs.get("unidade_uuid"))
        return kwargs


class AtividadeUpdateView(
    UUIDViewMixin, 
    UpdateView
):    
    '''
    Atualiza as informações de uma Atividade em uma Unidade
    '''
    model = Atividade
    form_class = AtividadeForm
    uuid_url_kwarg = "atividade_uuid"


    def form_valid(self, form):
        form.instance.unidade = Unidade.objects.get(uuid=self.kwargs.get("unidade_uuid"))
        return super().form_valid(form)

    
class AtividadeHistoricoListView(
    FilteredViewMixin,
    ListView
):
    '''
    Lista Idas e Retornos (Histórico) de Adolescente em uma determinada Atividade
    '''
    model = HistoricoAtividade
    filterset_class = HistoricoFilterset
    paginate_by: int = 40
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(atividade__uuid=self.kwargs['atividade_uuid']).order_by('-data_ida')
    
    
class AtividadeHistoricoUpdateView(
    UUIDViewMixin,
    InlineFormsetMixin,
    UpdateView
):
    '''
    Formulário de atualizaçõa de informações de uma Ida/Retorno (Histórico) de Adolecente em Determinada Atividade
    '''
    model = HistoricoAtividade
    form_class = HistoricoAtividadeForm
    uuid_url_kwarg = "historico_uuid"
    inlineformset_classes = {
        "anexos": AnexoAgendamentoAtividadeFormset
    }


class AtividadeHistoricoDeleteView(
    UUIDViewMixin,
    DeleteView
):
    '''
    Deleter uma Ida/Retorno (Histórico) de Adolecente em Determinada Atividade
    '''
    model = HistoricoAtividade
    uuid_url_kwarg = "historico_uuid"

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, f'Ida de {self.object.adolescente.nome} a {self.object.atividade.descricao} deletada com sucesso.')
        except Exception as e:    
            messages.error(self.request, f'Ida de {self.object.adolescente.nome} a {self.object.atividade.descricao} não pôde ser deletada.')
        return redirect(success_url)


class AdolescenteHistoricoAtividadeListView(ListView):
    '''
    Listar Idas e Retornos (Histórico) de Adolecente em Atividades de uma determinada Unidade
    '''
    model = HistoricoAtividade

    def get_queryset(self):
        entrada = EntradaAdolescente.objects.get(uuid=self.kwargs['entrada_uuid'])
        return super().get_queryset().filter(
            atividade__unidade = entrada.unidade, 
            adolescente = entrada.adolescente
            )
        


class AtividadeEnviarAdolescentesView(View):
    '''
    Lista Adolescentes de um determinado módulo para enviar para uma determinada Atividade (uuid da Atividade na URL)
    '''
    def get(self, request, *args, **kwargs):
        modulo = Modulo.objects.get(uuid=kwargs.get("modulo_uuid"))
        atividade = Atividade.objects.get(uuid=kwargs.get("atividade_uuid"))
        
        # todas idas sem retorno de adolescentes naquela atividade
        hist = HistoricoAtividade.objects.filter(
            adolescente__id__in=modulo.ids_adolescentes_lotados,
            atividade = atividade,   
            em_atividade = True
        )
        
        # trata o caso de adolescentes que podem ter passado mais de uma vez pela mesma unidade
        # ou seja: desconsidera atividades realizadas pelo adolescente em passagens anteriores
        entradas_atuais = modulo.entradas_atuais
        ids_atuais = []
        for h in hist:
            if entradas_atuais.filter(adolescente=h.adolescente, data_entrada__lt = h.data_ida).exists():
                ids_atuais.append(h.id)
                
        ids_adol_modulo_na_mesma_atividade = HistoricoAtividade.objects.filter(id__in=ids_atuais).values_list('adolescente__id', flat=True)
        
        
        context = {}
        context['entradas'] = modulo.entradas_atuais.exclude(adolescente__id__in=ids_adol_modulo_na_mesma_atividade)
        
        return render(
            request, 
            template_name=self.template_name, 
            context=context
        )
    

class AtividadeEnviarAdolescentesConfirmaView(View):
    '''
    Form de confirmação de envio de múltiplos Adolescentes de um módulo
    para uma determinada Atividade
    '''
    def first_setup(self, request, *args, **kwargs):
        self.atividade = Atividade.objects.get(uuid=kwargs.get("atividade_uuid"))       
        self.modulo = Modulo.objects.get(uuid=kwargs.get("modulo_uuid"))    
        self.uuids_adolescentes_selecionados = request.GET.getlist('adolescentes')        
        self.adolescentes = Adolescente.objects.filter(uuid__in=self.uuids_adolescentes_selecionados)


    def get(self, request, *args, **kwargs):
        # se não marcou ninguém na primeira tela, dá erro
        if not request.GET.getlist('adolescentes'):
            messages.error(request, f'Favor selecionar algum adolescente')
            return redirect(request.META.get('HTTP_REFERER'))
        
        self.first_setup(request, *args, **kwargs)
        context = {}
        context['adolescentes'] = self.adolescentes
        context['form'] = self.form = EnvioAdolescentesForm(
            modulo = self.modulo,
            adolescentes = self.adolescentes, 
            atividade = self.atividade,
        )

        return render(
            request, 
            template_name=self.template_name,
            context=context
        )

    def post(self, request, *args, **kwargs):
        self.first_setup(request, *args, **kwargs)
        
        context = {}
        context['form'] = self.form = EnvioAdolescentesForm(
            request.POST,
            request.FILES,
            modulo = self.modulo,
            adolescentes = self.adolescentes, 
            atividade = self.atividade,
        )
        context['adolescentes'] = self.adolescentes

        if self.form.is_valid():
            adolescentes = self.form.cleaned_data['adolescentes']
            atividade = self.form.cleaned_data['atividade']
            data_ida = self.form.cleaned_data['data_ida']
            observacoes = self.form.cleaned_data['observacoes']
            anexo = self.form.cleaned_data['anexo']
            
            for adolescente in adolescentes:
                # antes de criar o objeto Historico, verifica se não existe um agendamento semelhante
                agendamento = HistoricoAtividade.objects.filter(
                    modulo = self.modulo,
                    adolescente = adolescente,
                    atividade = atividade,
                    data_prevista_ida__date = data_ida, 
                    agendado = True, 
                    realizada = False,
                    em_atividade = False    
                )
                # se existe agendamento
                if agendamento.exists():
                    agendamento = agendamento.first()
                    agendamento.data_ida = data_ida
                    agendamento.observacoes = observacoes
                    agendamento.save()
                    if anexo is not None:
                        if isinstance(anexo, InMemoryUploadedFile) or isinstance(anexo, TemporaryUploadedFile):
                            anexo = agendamento.anexos.create(anexo=anexo)
                            anexo.save()
                        elif isinstance(anexo, AnexoHistoricoAtividade):                   
                            agendamento.anexos.create(anexo=anexo.anexo)

                else:
                    # se não existe, cria uma nova entrada de historico
                    try:
                        hist = HistoricoAtividade.objects.create(
                            modulo = self.modulo,
                            atividade=atividade,
                            adolescente=adolescente,
                            data_ida=data_ida,
                            observacoes=observacoes,
                        )
                        if anexo is not None:
                            
                            if isinstance(anexo, InMemoryUploadedFile) or isinstance(anexo, TemporaryUploadedFile):
                                anexo = hist.anexos.create(anexo=anexo)
                                anexo.save()
                            elif isinstance(anexo, AnexoHistoricoAtividade):                   
                                hist.anexos.create(anexo=anexo.anexo)
                        
                    except Exception as e:
                        messages.error(self.request, f'Erro ao enviar {adolescente.nome} para a atividade {atividade}. {get_error_message(e)}')
        
            return redirect(self.get_success_url())

        # se form invalido renderiza pagina com os erros no form
        return render(
            request, 
            template_name=self.template_name,
            context=context
        )


class AtividadeRetornarAdolescentesView(View):
    '''
    Lista adolescentes realizando determinada atividade, para retorno
    '''
    def get(self, request, *args, **kwargs):
        atividade = Atividade.objects.get(uuid=kwargs.get("atividade_uuid"))
        modulo = Modulo.objects.get(uuid=kwargs.get("modulo_uuid"))
        
        hist_na_atividade = HistoricoAtividade.objects.filter(
            adolescente__id__in=modulo.ids_adolescentes_lotados,
            atividade = atividade,
            em_atividade = True,
        )
        
        context = {'historicos' : hist_na_atividade}
        
        return render(
            request, 
            template_name=self.template_name, 
            context=context
        )

class AtividadeRetornarAdolescentesConfirmaView(View):
    '''
    Form de confirmação de retorno de múltiplos Adolescentes de um módulo
    de uma determinada Atividade
    '''
    def first_setup(self, request, *args, **kwargs):
        self.atividade = Atividade.objects.get(uuid=kwargs.get("atividade_uuid"))
        self.modulo = Modulo.objects.get(uuid=kwargs.get("modulo_uuid"))
        self.uuids_historicos_selecionados = request.GET.getlist('historicos')
        self.historicos = HistoricoAtividade.objects.filter(uuid__in=self.uuids_historicos_selecionados)

    def get(self, request, *args, **kwargs):
        # se não seleciona nenhum dá erro
        if not request.GET.getlist('historicos'):
            messages.error(request, f'Favor selecionar algum adolescente')
            return redirect(request.META.get('HTTP_REFERER'))

        self.first_setup(request, *args, **kwargs)

        context = {}
        context['historicos'] = self.historicos
        context['form'] = self.form = RetornoAdolescentesForm(
            modulo = self.modulo,
            historicos = self.historicos, 
            atividade = self.atividade,
        )
        
        return render(
            request, 
            template_name=self.template_name,
            context=context
        )

    def post(self, request, *args, **kwargs):
        self.first_setup(request, *args, **kwargs)
        
        context = {}
        context['historicos'] = self.historicos
        context['form'] = self.form = RetornoAdolescentesForm(
            request.POST,
            request.FILES,
            modulo = self.modulo,
            historicos = self.historicos, 
            atividade = self.atividade,
        )

        if self.form.is_valid():
            historicos = self.form.cleaned_data['historicos']
            data_retorno = self.form.cleaned_data['data_retorno']
            observacoes = self.form.cleaned_data['observacoes']
            anexo = self.form.cleaned_data['anexo']
            
            for historico in historicos:
                try:
                    historico.data_retorno = data_retorno
                    # nas observações apenas faz um append pra não sobrescrever observações anteriores
                    historico.observacoes += " - " + observacoes if historico.observacoes else observacoes                
                    historico.save()
                    if anexo is not None:
                        if isinstance(anexo, InMemoryUploadedFile) or isinstance(anexo, TemporaryUploadedFile):
                            anexo = historico.anexos.create(anexo=anexo)
                            anexo.save()
                        elif isinstance(anexo, AnexoHistoricoAtividade):                   
                            historico.anexos.create(anexo=anexo.anexo)
                except Exception as e:
                        messages.error(self.request, f'Erro ao retornar {historico.adolescente.nome} da a atividade {historico.atividade}. {get_error_message(e)}')
            return redirect(self.get_success_url())

        return render(
            request, 
            template_name=self.template_name,
            context=context
        )
    

class AgendamentoCriaMultiplosView(View):
    '''
    Formulario para agendamento de multiplos Adolescentes (de um módulo) em multiplas Atividades
    '''

    def get(self, request, *args, **kwargs):
        self.modulo = Modulo.objects.get(uuid=kwargs.get("modulo_uuid"))
        context = {}
        context['form'] = self.form = AgendamentoAtividadeForm(
            modulo = self.modulo
        )
        context["anexos"] = AnexoAgendamentoAtividadeFormset()
        
        return render(
            request, 
            template_name=self.template_name,
            context=context
        )

    def post(self, request, *args, **kwargs): 
        self.modulo = Modulo.objects.get(uuid=kwargs.get("modulo_uuid"))
        context = {}
        context['form'] = self.form = AgendamentoAtividadeForm(
            request.POST,
            request.FILES,
            modulo = self.modulo
        )
        context["anexos"] = anexos = AnexoAgendamentoAtividadeFormset(self.request.POST, self.request.FILES)

        
        if self.form.is_valid() and anexos.is_valid():
            datas = request.POST.getlist('data_prevista_ida')
            adolescentes = self.form.cleaned_data['adolescentes']
            servidores = self.form.cleaned_data['servidores']
            atividade = self.form.cleaned_data['atividade']
            observacoes_agendamento = self.form.cleaned_data['observacoes_agendamento']

            # Itera em adolescentes e datas para criar os agendamentos, em caso de erro injeta uma mensagem de erro
            for adolescente in adolescentes:
                for data in datas:
                    if data:
                        try:
                            hist = HistoricoAtividade.objects.create(
                                atividade = atividade,
                                adolescente = adolescente,
                                data_prevista_ida = data,
                                observacoes_agendamento = observacoes_agendamento,
                                modulo = self.modulo,
                            )

                            for servidor in servidores:
                                hist.servidores_relacionados.add(servidor)                            
                            hist.save()

                            pre_save_anexos = anexos.save(commit=False)
                            for anexo in pre_save_anexos:
                                hist.anexos.create(anexo = anexo.anexo)


                        except Exception as e:
                            from core.exceptions import get_error_message
                            messages.error(self.request, f'Erro ao criar agendamento de {adolescente.nome} na atividade {atividade}: {get_error_message(e)}')

            return redirect(self.get_success_url())
  
        return render(
            request, 
            template_name=self.template_name,
            context=context
        )



class AgendamentoListView(FilteredViewMixin, ListView):
    '''
    List Agendamentos
    '''
    model = HistoricoAtividade
    paginate_by: int = 30
    filterset_class = AgendamentoFilterset

    def get_queryset(self):
        return super().get_queryset().filter(
            agendado=True, 
        ).order_by('data_prevista_ida')


class AgendamentoEnviarUpdateView(
    UUIDViewMixin,
    UpdateView
):
    '''
    Form de Agendamento para efetivo envio para a atividade
    '''
    model = HistoricoAtividade
    form_class = AgendamentoEnviarForm
    uuid_url_kwarg = "historico_uuid"


class AgendamentoRetornarUpdateView(
    UUIDViewMixin,
    UpdateView
):
    '''
    Form de Agendamento para retorno da atividade
    '''
    model = HistoricoAtividade
    form_class = AgendamentoRetornarForm
    uuid_url_kwarg = "historico_uuid"


class AgendamentoUpdateView(
    UUIDViewMixin,
    InlineFormsetMixin,
    UpdateView
):
    '''
    Form para edição de informações de determinado agendamento
    '''
    model = HistoricoAtividade
    form_class = AgendamentoForm
    uuid_url_kwarg = "historico_uuid"
    inlineformset_classes = {
            "anexos": AnexoAgendamentoAtividadeFormset
            }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'modulo_uuid' in self.kwargs:
            kwargs['modulo'] = Modulo.objects.get(uuid=self.kwargs.get('modulo_uuid'))
        return kwargs

