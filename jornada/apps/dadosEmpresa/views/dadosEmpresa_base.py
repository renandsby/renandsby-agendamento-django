from posicao.models import RedeEmpresas


class RedeEmpresasFilterMixin:
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(rede__uuid=self.kwargs['rede_uuid'])

class RedeEmpresasFormBindMixin:
    def form_valid(self, form):
        form.instance.redeEmpresas = RedeEmpresas.objects.get(uuid=self.kwargs.get("rede_uuid"))
        return super().form_valid(form)