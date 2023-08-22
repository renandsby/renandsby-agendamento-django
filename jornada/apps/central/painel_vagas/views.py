from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from unidades.models import Unidade
from ._utils import adiciona_vagas

class VagasView(LoginRequiredMixin, View):
    
    def get(self, request):
        unidades_internacao = Unidade.objects.filter(tipo_unidade__descricao="Internação")
        unidades_atendimento_inicial = Unidade.objects.filter(tipo_unidade__descricao="Atendimento Inicial")
        unidades_semiliberdade = Unidade.objects.filter(tipo_unidade__descricao="Semiliberdade") 
        unidades_meio_aberto = Unidade.objects.filter(tipo_unidade__descricao="Meio Aberto") 
        context = {
            'unidades_internacao': adiciona_vagas(unidades_internacao),
            'unidades_semiliberdade': adiciona_vagas(unidades_semiliberdade),
            'unidades_meio_aberto': adiciona_vagas(unidades_meio_aberto),
            'unidades_atendimento_inicial': adiciona_vagas(unidades_atendimento_inicial),
        }

        return render(request, 'central/unidades/vagas.html', context)


class UnidadeAdolescentesView(LoginRequiredMixin, View):
    
    def get(self, request, **kwargs):
        unidade = Unidade.objects.get(uuid=kwargs.get('unidade_uuid'))
        context = {
            'unidade': unidade,
            'adolescentes': unidade.adolescentes_lotados_entradas,
            'adol_entrada_pendente': unidade.adolescentes_com_entrada_pendente,
            'adol_saida_pendente': unidade.adolescentes_com_saida_pendente,
        }
        
        return render(request, 'central/unidades/unidade_adolescentes.html', context)

