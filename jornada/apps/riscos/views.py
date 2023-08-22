
from django.views.generic import ListView, CreateView, UpdateView
from core.views import UUIDViewMixin

from .models import Risco
from .forms import RiscoForm

class RiscoListView(ListView):
    model = Risco

    
class RiscoCreateView(CreateView):
    model = Risco
    form_class = RiscoForm
    template_name = ""
    
    
class RiscoUpdateView(
    UUIDViewMixin, 
    UpdateView
):
    model = Risco
    form_class = RiscoForm
    uuid_url_kwarg = "risco_uuid"
    template_name = ""

