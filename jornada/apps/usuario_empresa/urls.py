from django.urls import path
from . import views

app_name = "usuario_empresa"

urlpatterns = [                
    path('', views.UsuarioEmpresaListView.as_view(), name='usuario-list'),
    path('create/', views.UsuarioEmpresaCreateView.as_view(), name='usuario-create'),
    path('<uuid:usuario_empresa_uuid>/update/', views.UsuarioEmpresaUpdateView.as_view(), name="usuario-update"),
]
