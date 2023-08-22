from . import pia

from .adolescente import (
    AdolescenteProntuarioCreateView,
    AdolescenteProntuarioDetailView,
    AdolescenteProntuarioListView,
    AdolescenteProntuarioToPrintDetailView,
    AdolescenteProntuarioUpdateView
)

from .atendimento_psicossocial import (
    AtendimentoPsicossocialProntuarioCreateView,
    AtendimentoPsicossocialProntuarioListView,
    AtendimentoPsicossocialProntuarioUpdateView
)

from .educacao import (
    EducacaoProntuarioCreateView,
    EducacaoProntuarioListView,
    EducacaoProntuarioUpdateView
)

from .endereco import (
    EnderecoProntuarioCreateView,
    EnderecoProntuarioListView,
    EnderecoProntuarioUpdateView
)

from .familiar import (
    FamiliarProntuarioCreateView,
    FamiliarProntuarioListView,
    FamiliarProntuarioUpdateView
)

from .historico import HistoricoListView

from .processo import (
    ProcessoProntuarioCreateView,
    ProcessoProntuarioListView,
    ProcessoProntuarioUpdateView,
    ProcessoProntuarioDeleteView,
)

from .risco import (
    RiscoProntuarioCreateView, 
    RiscoProntuarioListView,
    RiscoProntuarioUpdateView
)

from .telefone import (
    TelefoneProntuarioCreateView,
    TelefoneProntuarioListView,
    TelefoneProntuarioUpdateView, 
    TelefoneReportView
)

from .relatorio import (
    RelatorioProntuarioCreateView,
    RelatorioProntuarioListView,
    RelatorioProntuarioUpdateView,
    RelatorioProntuarioDeleteView
)

from .ocorrencias import (
    OcorrenciaProntuarioListView,
    OcorrenciaProntuarioDetailView
)

__all__ = [
    "AdolescenteProntuarioListView",
    "AdolescenteProntuarioCreateView",
    "AdolescenteProntuarioUpdateView",
    "AdolescenteProntuarioDetailView",
    "AdolescenteProntuarioDetailView",
    "AdolescenteProntuarioToPrintDetailView",
    "EnderecoProntuarioListView",
    "EnderecoProntuarioCreateView",
    "EnderecoProntuarioUpdateView",
    "AtendimentoPsicossocialProntuarioListView",
    "AtendimentoPsicossocialProntuarioCreateView",
    "AtendimentoPsicossocialProntuarioUpdateView",
    "EducacaoProntuarioListView",
    "EducacaoProntuarioCreateView",
    "EducacaoProntuarioUpdateView",
    "ProcessoProntuarioListView",
    "ProcessoProntuarioCreateView",
    "ProcessoProntuarioUpdateView",
    "ProcessoProntuarioDeleteView",
    "RiscoProntuarioListView",
    "RiscoProntuarioCreateView",
    "RiscoProntuarioUpdateView",
    "HistoricoListView",
    "TutorialListView",
    "TelefoneProntuarioCreateView",
    "TelefoneProntuarioListView",
    "TelefoneProntuarioUpdateView", 
    "TelefoneReportView",
    "RelatorioProntuarioListView",
    "RelatorioProntuarioCreateView",
    "RelatorioProntuarioUpdateView", 
    "RelatorioProntuarioDeleteView",
    "FamiliarProntuarioCreateView",
    "FamiliarProntuarioListView",
    "FamiliarProntuarioUpdateView",
    "OcorrenciaProntuarioListView",
    "OcorrenciaProntuarioDetailView"
]
