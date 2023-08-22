import glob
from typing import Any
from django import http
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from livro.views import (
    LivroPassagemPlantaoView,
    LivroRedirectView, 
    LivroUpdateView
)
from livro.models import Livro
from livro.forms import LivroImprimeDataForm


class UnidadeNovoPlantaoView(LoginRequiredMixin, LivroPassagemPlantaoView):
    template_name = "rotina_modulo/livro_c2/novo_plantao_form.html"

    def get_success_url(self):
        return reverse(
            "rotina_modulo:livro-c2-update",
            kwargs={
                "unidade_uuid": self.kwargs.get("unidade_uuid"),
                "livro_uuid": self.object.uuid,
            },
        )


class UnidadeLivroUpdateView(LoginRequiredMixin, LivroUpdateView):
    template_name = "rotina_modulo/livro_c2/livro_form.html"

    def get_success_url(self):
        if "novo_plantao" in self.request.POST:
            return reverse(
                "rotina_modulo:livro-c2-create",
                kwargs={
                    "unidade_uuid": self.kwargs.get("unidade_uuid"),
                },
            )
        
        return reverse(
            "rotina_modulo:livro-c2-update",
            kwargs={
                "unidade_uuid": self.kwargs.get("unidade_uuid"),
                "livro_uuid": self.kwargs.get("livro_uuid"),
            },
        )


class UnidadeLivroImprimeDataView(LoginRequiredMixin, TemplateView):
    template_name = "rotina_modulo/livro_c2/livro_imprime_data.html"
    
    def get(self, request, *args, **kwargs):
        form = LivroImprimeDataForm()
        return render(request, self.template_name, context={'form': form })
    
    def post(self, request, *args, **kwargs):
        
        form = LivroImprimeDataForm(request.POST)
        if form.is_valid():
            livro = Livro.objects.filter(
                data_abertura__date = form.cleaned_data['data'],
                unidade__uuid = kwargs.get('unidade_uuid'),
                modulo__isnull = True  
            )
            if not livro.exists():
                form._errors['data'] = ["Livro não encontrado"]
                return render(request, self.template_name, context={'form': form })
            
            livro = livro.first()
            return redirect(
                reverse(
                    "livro:livro-report",
                    kwargs={
                        "livro_uuid": livro.uuid,
                    },
                )
            )
        return render(request, self.template_name, context={'form': form })
    
    
    
class UnidadeLivroRedirectView(LoginRequiredMixin, LivroRedirectView):
    ...

