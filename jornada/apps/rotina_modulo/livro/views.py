from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, redirect, render
from django.views.generic import TemplateView
from livro.views import (LivroPassagemPlantaoView,LivroRedirectView, LivroUpdateView)
from livro.models import Livro
from livro.forms import LivroImprimeDataForm

class ModuloNovoPlantaoView(LoginRequiredMixin, LivroPassagemPlantaoView):
    template_name = "rotina_modulo/livro/novo_plantao_form.html"

    def get_success_url(self):
        return reverse(
            "rotina_modulo:livro-update",
            kwargs={
                "modulo_uuid": self.kwargs.get("modulo_uuid"),
                "livro_uuid": self.object.uuid,
            },
        )

class ModuloLivroImprimeDataView(LoginRequiredMixin, TemplateView):
    template_name = "rotina_modulo/livro/livro_imprime_data.html"
    
    def get(self, request, *args, **kwargs):
        form = LivroImprimeDataForm()
        return render(request, self.template_name, context={'form': form })
    
    def post(self, request, *args, **kwargs):
        
        form = LivroImprimeDataForm(request.POST)
        if form.is_valid():
            livro = Livro.objects.filter(
                data_abertura__date = form.cleaned_data['data'],
                modulo__uuid = kwargs.get('modulo_uuid')    
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


class ModuloLivroUpdateView(LoginRequiredMixin, LivroUpdateView):
    template_name = "rotina_modulo/livro/livro_form.html"

    def get_success_url(self):
        if 'novo_plantao' in self.request.POST:
            return reverse(
            "rotina_modulo:livro-create",
                kwargs={
                    "modulo_uuid": self.kwargs.get("modulo_uuid"),
                },
            )

        return reverse(
            "rotina_modulo:livro-update",
            kwargs={
                "modulo_uuid": self.kwargs.get("modulo_uuid"),
                "livro_uuid": self.kwargs.get("livro_uuid"),
            },
        )


class ModuloLivroRedirectView(LoginRequiredMixin, LivroRedirectView):
    ...
