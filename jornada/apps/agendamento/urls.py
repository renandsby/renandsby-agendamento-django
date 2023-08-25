from django.urls import path
from . import views

app_name = "agendamento"

urlpatterns = [   
    # path('', views.AgendamentoRedirectView.as_view(), name='home'),             
    path('list/', views.AgendamentoListView.as_view(), name='agendamento-list'),
    path('create/', views.AgendamentoCreateView.as_view(), name='agendamento-create'),
    path('<uuid:agendamento_uuid>/update/', views.AgendamentoUpdateView.as_view(), name="agendamento-update"),
]
