from django import forms
from datetime import datetime
from core.forms.widgets import CustomAttachmentInput
from agendamento.models import Agendamento
from posicao.models import RedeEmpresas
from agendamento.models import Agendamento

class AgendamentoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.initial["data_disponibilidade"] = datetime.now

   

    class Meta:
        model = Agendamento
        fields = "__all__"

