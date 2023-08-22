

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


from .endereco import (
    EnderecoProntuarioCreateView,
    EnderecoProntuarioListView,
    EnderecoProntuarioUpdateView
)


from .historico import HistoricoListView

from .processo import (
    ProcessoProntuarioCreateView,
    ProcessoProntuarioListView,
    ProcessoProntuarioUpdateView,
    ProcessoProntuarioDeleteView,
)


from .relatorio import (
    RelatorioProntuarioCreateView,
    RelatorioProntuarioListView,
    RelatorioProntuarioUpdateView,
    RelatorioProntuarioDeleteView
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
    "ProcessoProntuarioListView",
    "ProcessoProntuarioCreateView",
    "ProcessoProntuarioUpdateView",
    "ProcessoProntuarioDeleteView",
    "HistoricoListView",
    "TutorialListView",
    "RelatorioProntuarioListView",
    "RelatorioProntuarioCreateView",
    "RelatorioProntuarioUpdateView", 
    "RelatorioProntuarioDeleteView",
    "OcorrenciaProntuarioListView",
    "OcorrenciaProntuarioDetailView"
]
