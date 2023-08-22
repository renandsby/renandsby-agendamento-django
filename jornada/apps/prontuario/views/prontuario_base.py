from adolescentes.models import Adolescente



class AdolescenteFilterMixin:
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(adolescente__uuid=self.kwargs['adolescente_uuid'])

class AdolescenteFormBindMixin:
    def form_valid(self, form):
        form.instance.adolescente = Adolescente.objects.get(uuid=self.kwargs.get("adolescente_uuid"))
        return super().form_valid(form)