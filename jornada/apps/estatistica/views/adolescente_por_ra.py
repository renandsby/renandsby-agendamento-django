from django.views import View
from django.shortcuts import render
from adolescentes.models import Adolescente
from dominios.models import Bairro
from estatistica.dash.adolescentes.adolescente_por_ra import dashboard_adolescente_por_ra


class AdolescentePorRa(View):
    def get(self, request, *args, **kwargs):
        dashboard_adolescente_por_ra()
        data = {}
        try:
            # Adolescentes por RA
            adolescentes = list(Adolescente.objects.all())
            qs_bairro = list(Bairro.objects.all())
            bairros = [g for g in qs_bairro]
            ra_labels = []
            ra_values = []
            for bairro in bairros:
                ra_labels.append(bairro.nome)
                ra_values.append(
                    len(
                        [
                            adolescente
                            for adolescente in adolescentes
                            if adolescente.possui_entrada_ativa == True
                            and adolescente.endereco_atual.bairro_id == bairro.id
                        ]
                    )
                )

            data.update({'ra_labels': ra_labels, 'ra_values': ra_values})

        except:
            pass

        return render(self.request, 'estatistica/dashboard/adolescente_por_ra.html', context=data)
